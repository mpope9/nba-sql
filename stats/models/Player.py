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


Player model definition.
"""

from peewee import (
    IntegerField,
    CharField,
    Model
)


class Player(Model):

    player_id = IntegerField(primary_key=True)

    player_name = CharField(null=True)
    college = CharField(null=True)
    country = CharField(null=True)
    draft_year = CharField(null=True)
    draft_round = CharField(null=True)
    draft_number = CharField(null=True)

    class Meta:
        db_table = 'player'
