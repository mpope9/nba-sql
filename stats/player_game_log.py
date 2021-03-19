import requests
import urllib.parse

from peewee import fn
from settings import Settings
from models import PlayerGameLog
from constants import season_list, headers

class PlayerGameLogRequester:

    url = 'https://stats.nba.com/stats/playergamelogs'

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([PlayerGameLog])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayerGameLog], safe=True)

    def get_game_ids(self):
        """
        Returns a query containing the game_ids stored in the database.
        """
        return PlayerGameLog.select(fn.Distinct(PlayerGameLog.game_id))

    def populate_season(self, season_id):
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

        rows = []

        game_ids = set()

        # looping over data to insert into table
        for row in player_info:
            game_ids.add(row[6])
            new_row = {
                'season_id': int(season_id[:4]),
                'player_id': row[1],
                'team_id': row[3],
                'game_id': row[6],
                'game_date': row[7],
                'matchup': row[8],
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
            rows.append(new_row)

        PlayerGameLog.insert_many(rows).execute()

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
