from peewee import *

class Player(Model):
    player_id = IntegerField(primary_key = True)
    player_name = CharField(null = True)
    college = CharField(null = True)
    country = CharField(null = True)
    draft_year = CharField(null = True)
    draft_round = CharField(null = True)
    draft_number = CharField(null = True)

    class Meta:
        db_table = 'player'
