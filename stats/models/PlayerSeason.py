from peewee import *

class PlayerSeason(Model):
    season_id = CharField(null=False, index=True)  # added in at the end
    player_id = IntegerKey(null=False, index=True)
    team_id = IntegerField(null=False, index=True) # TODO: ForeignKey
    team_abbreviation = CharField(null = True)
    age = IntegerField(null = True)
    player_height = CharField(null = True)
    player_height_inches = IntegerField(null = True)
    player_weight = CharField(null = True)
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
        db_table = 'player_season'
