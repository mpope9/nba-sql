from peewee import (
    IntegerField,
    Model
)

class Season(Model):
    season_id = IntegerField(primary_key=True)

    class Meta:
        db_table= 'season'
