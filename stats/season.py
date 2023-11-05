"""
------------------------------------------------------------------------------
Copyright 2023 Matthew Pope

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------


Season builder.
"""

from models import Season

from db_utils import insert_many_on_conflict_ignore
from utils import season_id_to_int
from peewee import fn


class SeasonBuilder:

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([Season])

    def create_ddl(self):
        """
        Creates the season table.
        """
        self.settings.db.create_tables([Season], safe=True)

    def populate(self, seasons):
        """
        Populates the season table from the passed seasons. Ignores previous seasons
        that were already loaded.
        """

        season_ints = list(map(lambda p: self.season_to_row(p), seasons))
        insert_many_on_conflict_ignore(self.settings, Season, season_ints)

    def current_season_loaded(self):
        rows = Season.select(fn.MAX(Season.season_id)).execute()
        season_id = rows[0].season_id
        return season_id

    def season_to_row(self, season):
        season_id = season_id_to_int(season)
        return {'season_id': season_id}
