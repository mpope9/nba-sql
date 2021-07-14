from peewee import (
    ForeignKeyField,
    IntegerField,
    DateField,
    Model
)
from . import Team


class Game(Model):

    # Primary Key
    game_id = IntegerField(primary_key=True)

    # Foreign Keys
    team_id_home = ForeignKeyField(Team, index=True, null=False)
    team_id_away = ForeignKeyField(Team, index=True, null=False)

    # Indexes
    season_id = IntegerField(index=True, null=False)

    date = DateField(null=False)

    class Meta:
        db_table = 'game'
