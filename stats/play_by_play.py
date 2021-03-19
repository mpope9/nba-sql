import requests
import urllib.parse
import json

from settings import Settings
from models import PlayByPlay, Player
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

    def fetch_game(self, game_id):
        """
        Build GET REST request to the NBA for a game, iterate over the results and return them.
        """
        params = self.build_params(game_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        rows = []

        # looping over data to return.
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
                'player1_id': self.get_null_id(row[13]),
                'player1_team_id': self.get_null_id(row[15]),
                'player2_id': self.get_null_id(row[20]),
                'player2_team_id': self.get_null_id(row[22]),
                'player3_id': self.get_null_id(row[27]),
                'player3_team_id': self.get_null_id(row[29])
            }

            rows.append(new_row)
        return rows

    def insert_batch(self, rows, player_id_set):
        """
        Batch insertion of records.
        """

        ## It looks like the NBA API returns some bad data that 
        ## doesn't conform to their advertized schema. (team_id in the player_id spot).
        ## We can maybe get away with ignoring it.
        ## Check if id is in player_id cache.
        ## We need to preserve the row in general becuase it could still have good data
        ## for the correctly returned players.
        for row in rows:
            for key in ['player1_id', 'player2_id', 'player3_id']:
                if row[key] != None and row[key] not in player_id_set:
                    row[key] = None
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

    def get_null_id(self, id):
        """
        This endpoint will return a player's id or player's team id as 0 sometimes. 
        We will store 'null', as 0 breaks the foriegn key constraint.
        """
        if id is 0:
            return None
        return id
