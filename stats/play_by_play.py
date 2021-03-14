import requests
import urllib.parse

from settings import Settings
from models import PlayByPlay
from constants import season_list, headers

class PlayByPlayRequester:

    url = 'https://stats.nba.com/stats/playbyplayv2'

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([PlayByPlay])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayerGameLog], safe=True)

    def populate_season(self, game_id):
        """
        Build GET REST request to the NBA for a game, iterate over the results,
        store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        print("%s" % player_info)
        rows = []

        # looping over data to insert into table
        #for row in player_info:
        #    new_row = {
        #    }
        #    rows.append(new_row)

        #PlayByPlay.insert_many(rows).execute()

    def build_params(self, game_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'EndPeriod': '',
            'GameId': game_id,
            'StartPeriod': ''
        }
