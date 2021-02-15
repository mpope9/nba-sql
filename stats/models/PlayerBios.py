from peewee import *
#from models import BaseModel

class PlayerBios(Model):
    season_id = CharField(null=True)  # added in at the end
    player_id = IntegerField(null = True)
    player_name = CharField(null = True)
    team_id = IntegerField(null = True)
    team_abbreviation = CharField(null = True)
    age = IntegerField(null = True)
    player_height = CharField(null = True)
    player_height_inches = IntegerField(null = True)
    player_weight = CharField(null = True)
    college = CharField(null = True)
    country = CharField(null = True)
    draft_year = CharField(null = True)
    draft_round = CharField(null = True)
    draft_number = CharField(null = True)
    gp = IntegerField(null = True)
    pts = FloatField(null = True)
    reb = FloatField(null = True)
    ast = FloatField(null = True)
    net_rating = FloatField(null = True)
    oreb_pct = FloatField(null = True)
    dreb_pct = FloatField(null = True)
    usg_pct = FloatField(null = True)
    ts_pct = FloatField(null = True)
    ast_pct = FloatField(null = True)
	
    class Meta:
        db_table = 'player_bios'
