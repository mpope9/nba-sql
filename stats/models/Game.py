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


Game model definition.
"""

from peewee import (
    ForeignKeyField,
    IntegerField,
    DateField,
    Model
)
from . import Team


class Game(Model):

    # Primary Key
    game_id = IntegerField(primary_key=True)

    # Foreign Keys
    team_id_home = ForeignKeyField(Team, index=True, null=False, column_name='team_id_home')
    team_id_away = ForeignKeyField(Team, index=True, null=False, column_name='team_id_away')
    team_id_winner = ForeignKeyField(Team, index=True, null=False, column_name='team_id_winner')
    team_id_loser = ForeignKeyField(Team, index=True, null=False, column_name='team_id_loser')

    # Indexes
    season_id = IntegerField(index=True, null=False)

    date = DateField(null=False)

    class Meta:
        db_table = 'game'
