from peewee import *

class Player(Model):

    id = IntegerField(primary_key=True)

    class Meta:
        db_table = 'play_by_play'
