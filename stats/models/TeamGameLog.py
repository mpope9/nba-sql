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


TeamGameLog model definition.
"""

from peewee import (
    ForeignKeyField,
    IntegerField,
    CharField,
    FloatField,
    Model,
    CompositeKey
)
from . import Team
from . import Game


class TeamGameLog(Model):

    # Composite PK Fields
    team_id = ForeignKeyField(Team, index=True)
    game_id = ForeignKeyField(Game, index=True)

    # Indexes
    season_id = IntegerField(index=True)

    game_date = CharField(null=True)
    matchup = CharField(null=True)
    wl = CharField(null=True)
    min = FloatField(null=True)
    fgm = FloatField(null=True)
    fga = FloatField(null=True)
    fg_pct = FloatField(null=True)
    fg3m = FloatField(null=True)
    fg3a = FloatField(null=True)
    fg3_pct = FloatField(null=True)
    ftm = FloatField(null=True)
    fta = FloatField(null=True)
    ft_pct = FloatField(null=True)
    oreb = FloatField(null=True)
    dreb = FloatField(null=True)
    reb = FloatField(null=True)
    ast = FloatField(null=True)
    stl = FloatField(null=True)
    blk = FloatField(null=True)
    tov = FloatField(null=True)
    pf = FloatField(null=True)
    pts = FloatField(null=True)
    plus_minus = FloatField(null=True)
    video_available = IntegerField(null=True)

    class Meta:
        db_table = 'team_game_log'
        primary_key = CompositeKey(
            'team_id',
            'game_id',
        )
