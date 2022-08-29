import requests
import urllib.parse

from db_utils import insert_many
from utils import get_rowset_mapping, column_names_from_table, season_id_to_int
from models import PlayerGameLog, PlayerGameLogTemp
from game import GameEntry
from general_requester import GenericRequester
from constants import headers


class PlayerGameLogRequester(GenericRequester):
    """
    This class builds player game data from a season.
    As an optimization, we also build a set of game data.
    This is so we can build the game table without having to
    make a request for every game. We probably shouldn't
    do this, as this relys on data from the endpoint and if that
    changes this logic also must. But its fine for now...
    """

    url = 'https://stats.nba.com/stats/playergamelogs'
    game_set = set()

    def __init__(self, settings):
        """
        Constructor.
        """
        super().__init__(settings, self.url, PlayerGameLog)
        # TODO: this conflicts with a fresh db.
        self.settings.db.bind([PlayerGameLogTemp])
        self.settings.db.create_tables([PlayerGameLogTemp], safe=True)

    def create_ddl(self):
        """
        Override method to setup temp table.
        """
        super().create_ddl()
 
    def populate_temp(self):
        """
        Bulk insert.
        """
        insert_many(self.settings, PlayerGameLogTemp, self.rows)
        ## TODO: should set rows to []?

    def get_game_set(self):
        """
        Returns a the set of game ids.
        """
        return self.game_set

    def get_rows(self):
        """
        Returns the stored row list, to be inserted after the game data.
        """
        return self.rows

    def set_game_set(self, set_new):
        """
        Sets the game set.
        """
        self.game_set = set_new

    def get_team_player_id_set(self, temp_table=False):
        """
        Returns a set of team id and player ids, used for the shot_chart_detail api.
        """
        s = set()

        if temp_table:
            table = PlayerGameLogTemp
        else:
            table = PlayerGameLog

        tid = table.team_id
        pid = table.player_id

        for player_game_log in table.select(tid, pid).group_by(tid, pid):
            s.add((player_game_log.team_id, player_game_log.player_id))

        return s

    def temp_table_except_predicate(self):
        """
        This runs an EXCEPT between the temp table and the non-temp table to find
        the new games.
        """
        regular_query = PlayerGameLog.select(PlayerGameLog.game_id)
        temp_query = PlayerGameLogTemp.select(PlayerGameLogTemp.game_id)

        expt = temp_query - regular_query

        return expt.select_from(expt.c.game_id)

    def fetch_season(self, season_id):
        """
        Build GET REST request to the NBA for a season,
        iterate over the results,
        store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        result_sets = response['resultSets'][0]
        rowset = result_sets['rowSet']

        season_int = season_id_to_int(season_id)
        column_names = column_names_from_table(self.settings.db, self.table._meta.table_name)

        column_mapping = get_rowset_mapping(result_sets, column_names)

        rowset_mapping = get_rowset_mapping(result_sets, self.local_resultset_rows())

        # looping over data to insert into table
        for row in rowset:

            matchup = row[rowset_mapping['MATCHUP']]
            wl = row[rowset_mapping['WL']]
            team_id = row[rowset_mapping['TEAM_ID']]
            game_date = row[rowset_mapping['GAME_DATE']]
            game_id = row[rowset_mapping['GAME_ID']]

            # Checking matchup for home team.
            if '@' in matchup:
                if wl == "W":
                    winner = team_id
                    loser = ""
                else:
                    winner = ""
                    loser = team_id
                self.game_set.add(
                    GameEntry(
                        season_id=season_int, 
                        game_id=game_id,
                        game_date=game_date,
                        matchup_in=matchup,
                        winner=winner, 
                        loser=loser))

            new_row = {column_name: row[row_index] for column_name, row_index in column_mapping.items()}
            new_row['season_id'] = season_int
            self.rows.append(new_row)

    def build_params(self, season_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'DateFrom': '',
            'DateTo': '',
            'GameSegment': '',
            'LastNGames': '',
            'LeagueID': '00',
            'Location': '',
            'MeasureType': '',
            'Month': '',
            'OppTeamID': '',
            'Outcome': '',
            'PORound': '',
            'PerMode': '',
            'Period': '',
            'PlayerID': '',
            'Season': season_id,
            'SeasonSegment': '',
            'SeasonType': 'Regular Season',
            'ShotClockRange': '',
            'TeamID': '',
            'VsConference': '',
            'VsDivision': ''
        }

    def local_resultset_rows(self):
        """
        Returns list of the specific rows that we want to pull from the request.
        """

        return [
            'MATCHUP',
            'WL',
            'TEAM_ID',
            'GAME_ID',
            'GAME_DATE'
        ]

    def insert_from_temp_into_reg(self):
        """
        Inserts values from the temp table into the regular table that don't exist
        in the regular table already.

        THERE HAS TO BE A BETTER WAY OF DEFINING ALL FIELDS.
        """
        predicate = PlayerGameLog.select(PlayerGameLog.game_id)

        (PlayerGameLog.insert_from(
            PlayerGameLogTemp
                .select()
                .where(PlayerGameLogTemp.game_id.not_in(predicate)),
            fields=[
                PlayerGameLog.player_id,
                PlayerGameLog.game_id,
                PlayerGameLog.team_id,
                PlayerGameLog.season_id,
                PlayerGameLog.wl,
                PlayerGameLog.min,
                PlayerGameLog.fgm,
                PlayerGameLog.fga,
                PlayerGameLog.fg_pct,
                PlayerGameLog.fg3m,
                PlayerGameLog.fg3a,
                PlayerGameLog.fg3_pct,
                PlayerGameLog.ftm,
                PlayerGameLog.fta,
                PlayerGameLog.ft_pct,
                PlayerGameLog.oreb,
                PlayerGameLog.dreb,
                PlayerGameLog.reb,
                PlayerGameLog.ast,
                PlayerGameLog.tov,
                PlayerGameLog.stl,
                PlayerGameLog.blk,
                PlayerGameLog.blka,
                PlayerGameLog.pf,
                PlayerGameLog.pfd,
                PlayerGameLog.pts,
                PlayerGameLog.plus_minus,
                PlayerGameLog.nba_fantasy_pts,
                PlayerGameLog.dd2,
                PlayerGameLog.td3
            ]
        )).execute()
