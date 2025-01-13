"""
------------------------------------------------------------------------------
Copyright 2023 Matthew Pope

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------


PlayByPlayV3 object requester and builder.

This has a simpler schema than PlayByPlay
"""

import requests
import urllib.parse

from models import PlayByPlayV3
from constants import headers
from db_utils import insert_many


class PlayByPlayV3Requester:

    url = 'https://stats.nba.com/stats/playbyplayv3'

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([PlayByPlayV3])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([PlayByPlayV3], safe=True)

    def fetch_game(self, game_id):
        """
        Build GET REST request to the NBA for a game, iterate over
        the results and return them.
        """
        params = self.build_params(game_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

        response = requests.get(url=self.url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['game']['actions']
        game_id = response['game']['gameId']

        rows = []

        # looping over data to return.
        for row in player_info:
            new_row = {
                'game_id': game_id,
                'action_number': row['actionNumber'],
                'clock': row['clock'],
                'period': row['period'],
                'team_id': self.get_null_id(row['teamId']),
                'player_id': self.get_null_id(row['personId']),
                'x_legacy': row['xLegacy'],
                'y_legacy': row['yLegacy'],
                'shot_distance': row['shotDistance'],
                'shot_result': row['shotResult'],
                'is_field_goal': row['isFieldGoal'],
                'score_home': row['scoreHome'],
                'score_away': row['scoreAway'],
                'points_total': row['pointsTotal'],
                'location': row['location'],
                'description': row['description'],
                'action_type': row['actionType'],
                'sub_type': row['subType']
            }
            rows.append(new_row)
        return rows

    def insert_batch(self, rows):
        """
        Batch insertion of records.
        """
        insert_many(self.settings, PlayByPlayV3, rows)

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
        This endpoint will return a player's id or player's team id as 0
        sometimes.  We will store 'null', as 0 breaks the foriegn key
        constraint.
        """
        if id == 0:
            return None
        return id
