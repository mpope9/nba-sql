import requests
import urllib.parse

from utils import get_rowset_mapping, column_names_from_table, season_id_to_int
from models import PlayerGameLog
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

    def get_team_player_id_set(self):
        """
        Returns a set of team id and player ids, used for the shot_chart_detail api.
        """
        s = set()
        tid = PlayerGameLog.team_id
        pid = PlayerGameLog.player_id

        for player_game_log in PlayerGameLog.select(tid, pid).group_by(tid, pid):
            s.add((player_game_log.team_id, player_game_log.player_id))

        return s

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

        # looping over data to insert into table
        for row in rowset:
            # Checking matchup for home team.
            if '@' in row[9]:
                if row[10] == "W":
                    winner = row[4]
                    loser = ""
                else:
                    winner = ""
                    loser = row[4]
                self.game_set.add(GameEntry(season_id=season_int, game_id=row[7], game_date=row[8], matchup_in=row[9],
                                            winner=winner, loser=loser))

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
