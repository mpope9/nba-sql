import requests
import urllib.parse

from settings import Settings
from models import PlayerSeason
from constants import season_list, headers

class PlayerSeasonRequester:

    per_mode = 'Totals'
    player_info_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats'

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        self.settings = settings
        self.settings.db.bind([PlayerSeason])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayerSeason], safe=True)

    def populate_season(self, season_id):
        """
        Build GET REST request to the NBA for a season, iterate over the results,
        store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

	    # json response
        response = requests.get(url=self.player_info_url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        rows = []

        # looping over data to insert into table
        for row in player_info:
            new_row = {
                'season_id': int(season_id[:4]),
                'player_id': row[0],
                'team_id': row[2],
                'age': row[4],
                'player_height': row[5],
                'player_height_inches': row[6],
                'player_weight': row[7],
                'gp': row[13],
                'pts': row[14],
                'reb': row[15],
                'ast': row[16],
                'net_rating': row[17],
                'oreb_pct': row[18],
                'dreb_pct': row[19],
                'usg_pct': row[20],
                'ts_pct': row[21],
                'ast_pct': row[22]
            }
            rows.append(new_row)
        PlayerSeason.insert_many(rows).execute()

    def build_params(self, season_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'College': '',
            'Conference': '',
            'Country': '',
            'DateFrom': '',
            'DateTo': '',
            'Division': '',
            'DraftPick': '',
            'DraftYear': '',
            'GameScope': '',
            'GameSegment': '',
            'Height': '',
            'LastNGames': '0',
            'LeagueID': '00',
            'Location': '',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PerMode': self.per_mode,
            'Period': '0',
            'PlayerExperience': '',
            'PlayerPosition': '',
            'Season': season_id,
            'SeasonSegment': '',
            'SeasonType': 'Regular+Season',
            'ShotClockRange': '',
            'StarterBench': '',
            'TeamID': '0',
            'VsConference': '',
            'VsDivision': '',
            'Weight': ''
        }
