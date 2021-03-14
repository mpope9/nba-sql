import requests
import urllib.parse
import json

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
        self.settings.db.create_tables([PlayByPlay], safe=True)

    def populate_season(self, game_id):
        """
        Build GET REST request to the NBA for a game, iterate over the results,
        store in the database.
        """
        params = self.build_params(game_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        rows = []

        # looping over data to insert into table
        for row in player_info:
            new_row = {
                'game_id': row[0],
                'event_num': row[1],
                'event_msg_type': row[2],
                'event_msg_action_type': row[3],
                'period': row[4],
                'wc_time': row[5],
                'home_description': row[7],
                'neutral_description': row[8],
                'visitor_description': row[9],
                'score': row[10],
                'score_margin': row[11],
                'player1_id': row[13],
                'player1_team_id': row[15],
                'player2_id': row[20],
                'player2_team_id': row[22],
                'player3_id': row[27],
                'player3_team_id': row[29]
            }
            rows.append(new_row)

        PlayByPlay.insert_many(rows).execute()

    def build_params(self, game_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'EndPeriod': 6,
            'GameId': game_id,
            'StartPeriod': 1
        }
