import requests
import urllib.parse

from models import PlayerGameLog
from constants import headers
from game import GameEntry


class PlayerGameLogRequester:
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
    rows = []

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([PlayerGameLog])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayerGameLog], safe=True)

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

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        season_int = int(season_id[:4])

        # looping over data to insert into table
        for row in player_info:
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

            new_row = {
                'season_id': season_int,
                'player_id': row[1],
                'team_id': row[4],
                'game_id': int(row[7]),
                'wl': row[10],
                'min': row[11],
                'fgm': row[12],
                'fga': row[13],
                'fg_pct': row[14],
                'fg3m': row[15],
                'fg3a': row[16],
                'fg3_pct': row[17],
                'ftm': row[18],
                'fta': row[19],
                'ft_pct': row[20],
                'oreb': row[21],
                'dreb': row[22],
                'reb': row[23],
                'ast': row[24],
                'tov': row[25],
                'stl': row[26],
                'blk': row[27],
                'blka': row[28],
                'pf': row[29],
                'pfd': row[30],
                'pts': row[31],
                'plus_minus': row[32],
                'nba_fantasy_pts': row[33],
                'dd2': row[34],
                'td3': row[35]
            }
            self.rows.append(new_row)

    def store_rows(self):
        """
        Stores the rows that have been fetched.
        """
        PlayerGameLog.insert_many(self.rows).execute()

        # Is this how to 'free' memory?
        self.rows = []

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
