from peewee import *
from . import Player
from . import Team

class PlayerSeason(Model):

    ## Composite PK Fields
    player_id = ForeignKeyField(Player, index=True)
    season_id = IntegerField(null=False, index=True)
    team_id = ForeignKeyField(Team, index=True, null=True)

    age = IntegerField(null=True)
    player_height = CharField(null=True)
    player_height_inches = IntegerField(null=True)
    player_weight = CharField(null=True)
    gp = IntegerField(null=True)
    pts = FloatField(null=True)
    reb = FloatField(null=True)
    ast = FloatField(null=True)
    net_rating = FloatField(null=True)
    oreb_pct = FloatField(null=True)
    dreb_pct = FloatField(null=True)
    usg_pct = FloatField(null=True)
    ts_pct = FloatField(null=True)
    ast_pct = FloatField(null=True)
	
    class Meta:
        db_table = 'player_season'
        primary_key = CompositeKey(
            'player_id',
            'season_id',
            'team_id'
        )
