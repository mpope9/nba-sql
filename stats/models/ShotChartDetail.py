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


ShotChartDetail model definition.
"""

from peewee import (
    ForeignKeyField,
    IntegerField,
    BooleanField,
    FloatField,
    DecimalField,
    CharField,
    Model
)
from . import Team
from . import Game
from . import Player


class ShotChartDetail(Model):

    # Autogenerated id column here.

    game_id = ForeignKeyField(Game, index=True, unique=False)
    player_id = ForeignKeyField(Player, index=True, unique=False)
    team_id = ForeignKeyField(Team, index=True, unique=False)

    game_event_id = IntegerField(null=True)
    period = IntegerField(null=True)
    minutes_remaining = IntegerField(null=True)
    seconds_remaining = IntegerField(null=True)
    event_type = CharField(null=True)
    action_type = CharField(null=True)
    shot_type = CharField(null=True)
    shot_zone_basic = CharField(null=True)
    shot_zone_area = CharField(null=True)
    shot_zone_range = CharField(null=True)
    shot_distance = FloatField(null=True)
    loc_x = DecimalField(null=True)
    loc_y = DecimalField(null=True)
    shot_attempted_flag = BooleanField(null=True)
    shot_made_flag = BooleanField(null=True)
    htm = CharField(null=True)
    vtm = CharField(null=True)

    class Meta:
        db_table = 'shot_chart_detail'
