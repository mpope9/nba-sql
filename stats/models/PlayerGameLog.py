from peewee import *
from . import Player
from . import Team
from . import Game

class PlayerGameLog(Model):
    
    ## Composite PK Fields
    player_id = ForeignKeyField(Player, index=True)
    game_id = ForeignKeyField(Game, null=True)

    ## Foreign Keys
    team_id = ForeignKeyField(Team, index=True)

    ## Indexes
    season_id = IntegerField(index=True)

    wl = FixedCharField(null=True, max_length=1)
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

    class Meta:
        db_table = 'player_game_log'
        primary_key = CompositeKey(
            'player_id',
            'game_id'
        )
