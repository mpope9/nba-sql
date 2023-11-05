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


PlayByPlay model definition.
"""

from peewee import ForeignKeyField, IntegerField, CharField, Model
from . import EventMessageType
from . import Player
from . import Team
from . import Game


class PlayByPlay(Model):

    # Indexes
    game_id = ForeignKeyField(Game, index=True)

    event_num = IntegerField()
    event_msg_type = ForeignKeyField(EventMessageType, index=True)
    event_msg_action_type = IntegerField(index=True)
    period = IntegerField()

    # Why not time field? WELL, some times like "24:11 PM" are returned.
    wc_time = CharField()

    home_description = CharField(null=True)
    neutral_description = CharField(null=True)
    visitor_description = CharField(null=True)
    score = CharField(null=True)
    score_margin = CharField(null=True)

    player1_id = ForeignKeyField(Player, index=True, null=True)
    player1_team_id = ForeignKeyField(Team, index=True, null=True)

    player2_id = ForeignKeyField(Player, index=True, null=True)
    player2_team_id = ForeignKeyField(Team, index=True, null=True)

    player3_id = ForeignKeyField(Player, index=True, null=True)
    player3_team_id = ForeignKeyField(Team, index=True, null=True)

    class Meta:
        db_table = 'play_by_play'
