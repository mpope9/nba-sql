from peewee import (
    IntegerField,
    CharField,
    Model,
)


class Team(Model):

    # Primary Key
    team_id = IntegerField(primary_key=True)

    abbreviation = CharField(null=True)
    nickname = CharField(null=True)
    year_founded = CharField(null=True)
    city = CharField(null=True)

    class Meta:
        db_table = 'team'
