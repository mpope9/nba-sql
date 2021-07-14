from peewee import (
    ForeignKeyField,
    IntegerField,
    CharField,
    FloatField,
    Model
)
from . import Player
from . import Team


class PlayerSeason(Model):

    # Defaulting to auto generated id column. We do this because
    # team_id is nullable for players in a season and that breaks the
    # team table's Primary Key constraint.

    # Composite Unique Index
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
        indexes = (
            (('player_id', 'season_id', 'team_id'), True),
        )
