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
    yearfounded = CharField(null=True)
    city = CharField(null=True)

    class Meta:
        db_table = 'team'
