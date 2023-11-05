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


PlayerGeneralTraditionalTotal model definition.
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


class PlayerGeneralTraditionalTotal(Model):

    # Defaulting to auto generated id column. We do this because
    # team_id is nullable for players in a season and that breaks the
    # team table's Primary Key constraint.

    # Composite Unique Index
    player_id = ForeignKeyField(Player, null=False, index=True)
    season_id = IntegerField(null=False, index=True)
    team_id = ForeignKeyField(Team, index=True, null=True)

    age = IntegerField(null=True)
    gp = IntegerField(null=True)
    w = IntegerField(null=True)
    l = IntegerField(null=True) # NOQA
    w_pct = FloatField(null=True)
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
    tov = FloatField(null=True)
    stl = FloatField(null=True)
    blk = FloatField(null=True)
    blka = FloatField(null=True)
    pf = FloatField(null=True)
    pfd = FloatField(null=True)
    pts = FloatField(null=True)
    plus_minus = FloatField(null=True)
    nba_fantasy_pts = FloatField(null=True)
    dd2 = FloatField(null=True)
    td3 = FloatField(null=True)
    gp_rank = IntegerField(null=True)
    w_rank = IntegerField(null=True)
    l_rank = IntegerField(null=True)
    w_pct_rank = IntegerField(null=True)
    min_rank = IntegerField(null=True)
    fgm_rank = IntegerField(null=True)
    fga_rank = IntegerField(null=True)
    fg_pct_rank = IntegerField(null=True)
    fg3m_rank = IntegerField(null=True)
    fg3a_rank = IntegerField(null=True)
    fg3_pct_rank = IntegerField(null=True)
    ftm_rank = IntegerField(null=True)
    fta_rank = IntegerField(null=True)
    ft_pct_rank = IntegerField(null=True)
    oreb_rank = IntegerField(null=True)
    dreb_rank = IntegerField(null=True)
    reb_rank = IntegerField(null=True)
    ast_rank = IntegerField(null=True)
    tov_rank = IntegerField(null=True)
    stl_rank = IntegerField(null=True)
    blk_rank = IntegerField(null=True)
    blka_rank = IntegerField(null=True)
    pf_rank = IntegerField(null=True)
    pfd_rank = IntegerField(null=True)
    pts_rank = IntegerField(null=True)
    plus_minus_rank = IntegerField(null=True)
    nba_fantasy_pts_rank = IntegerField(null=True)
    dd2_rank = IntegerField(null=True)
    td3_rank = IntegerField(null=True)

    # This column is obscelete but it is kept for
    # backwards compatiblity. It is no longer returned
    # by the NBA API.
    cfid = IntegerField(null=True)

    cfparams = CharField(null=True)

    class Meta:
        db_table = 'player_general_traditional_total'
        indexes = (
            (('player_id', 'season_id', 'team_id'), True),
        )
