import requests
import urllib.parse

from peewee import fn
from settings import Settings
from models import PlayerGameLog
from constants import season_list, headers

class PlayerGameLogRequester:
    """
    This class builds player game data from a season. As an optimization, we also
    build a set of game data. This is so we can build the game table without having to
    make a request for every game. We probably shouldn't do this, as this relys on data
    from the endpoint and if that changes this logic also must. But its fine for now...
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
        Build GET REST request to the NBA for a season, iterate over the results,
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
            if '@' in row[8]:
                self.game_set.add((season_int, row[6], row[7], row[8]))

            new_row = {
                'season_id': season_int,
                'player_id': row[1],
                'team_id': row[3],
                'game_id': int(row[6]),
                'wl': row[9],
                'min': row[10],
                'fgm': row[11],
                'fga': row[12],
                'fg_pct': row[13],
                'fg3m': row[14],
                'fg3a': row[15],
                'fg3_pct': row[16],
                'ftm': row[17],
                'fta': row[18],
                'ft_pct': row[19],
                'oreb': row[20],
                'dreb': row[21],
                'reb': row[22],
                'ast': row[23],
                'tov': row[24],
                'stl': row[25],
                'blk': row[26],
                'blka': row[27],
                'pf': row[28],
                'pfd': row[29],
                'pts': row[30],
                'plus_minus': row[31],
                'nba_fantasy_pts': row[32],
                'dd2': row[33],
                'td3': row[34]
            }
            self.rows.append(new_row)

    def store_rows(self):
        """
        Stores the rows that have been fetched.
        """
        PlayerGameLog.insert_many(self.rows).execute()
        self.rows = [] # Is this how to 'free' memory?

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
