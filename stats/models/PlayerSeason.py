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


PlayerSeason model definition.
"""

from peewee import (
    ForeignKeyField,
    IntegerField,
    CharField,
    FloatField,
    Model
)
from . import Player
from . import Team


class PlayerSeason(Model):

    # Defaulting to auto generated id column. We do this because
    # team_id is nullable for players in a season and that breaks the
    # team table's Primary Key constraint.

    # Composite Unique Index
    player_id = ForeignKeyField(Player, index=True)
    season_id = IntegerField(null=False, index=True)
    team_id = ForeignKeyField(Team, index=True, null=True)

    age = IntegerField(null=True)
    player_height = CharField(null=True)
    player_height_inches = IntegerField(null=True)
    player_weight = CharField(null=True)
    gp = IntegerField(null=True)
    pts = FloatField(null=True)
    reb = FloatField(null=True)
    ast = FloatField(null=True)
    net_rating = FloatField(null=True)
    oreb_pct = FloatField(null=True)
    dreb_pct = FloatField(null=True)
    usg_pct = FloatField(null=True)
    ts_pct = FloatField(null=True)
    ast_pct = FloatField(null=True)

    class Meta:
        db_table = 'player_season'
        indexes = (
            (('player_id', 'season_id', 'team_id'), False),
        )
