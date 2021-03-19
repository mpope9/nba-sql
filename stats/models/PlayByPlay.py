from peewee import *
from . import EventMessageType
from . import Player
from . import Team

class PlayByPlay(Model):

    ## Indexes
    game_id = IntegerField(index=True)

    event_num = IntegerField()
    event_msg_type = ForeignKeyField(EventMessageType, index=True)
    event_msg_action_type = IntegerField(index=True)
    period = IntegerField()
    wc_time = CharField() # Why not time field? WELL, some times like "24:11 PM" are returned.
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
