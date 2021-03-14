from peewee import *

class TeamSeason(Model):

    team_id = IntegerField(primary_key=True)

    ## Indexes
    season_id = IntegerField(index=True)

    owner = CharField(null=True)
    general_manager = CharField(null=True)
    head_coach = CharField(null=True)
    dleague_affiliation = CharField(null=True)

    class Meta:
        db_table = 'team'
