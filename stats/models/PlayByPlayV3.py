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


PlayByPlayV3 model definition.
"""

from peewee import ForeignKeyField, IntegerField, CharField, Model
from . import Player
from . import Game
from . import Team

class PlayByPlayV3(Model):

    # Indexes
    game_id = ForeignKeyField(Game, index=True, null=False)
    player_id = ForeignKeyField(Player, index=True, null=True)
    team_id = ForeignKeyField(Team, index=True, null=True)

    action_number = CharField()
    clock = CharField()
    period = CharField()
    x_legacy = CharField()
    y_legacy = CharField()
    shot_distance = CharField()
    shot_result = CharField()
    is_field_goal = CharField()
    score_home = CharField()
    score_away = CharField()
    points_total = CharField()
    location = CharField()
    description = CharField()
    action_type = CharField()
    sub_type = CharField()

    class Meta:
        db_table = 'play_by_playv3'

