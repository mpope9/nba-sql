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


Game builder.
"""

from models import Game
from constants import team_abbrev_mapping
from collections import namedtuple
from db_utils import insert_many, insert_many_on_conflict_ignore


GameEntry = namedtuple("GameEntry", "season_id, game_id, game_date, matchup_in, winner, loser")


class GameBuilder:

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([Game])

    def create_ddl(self):
        """
        Creates the game table from the model.
        """
        self.settings.db.create_tables([Game], safe=True)

    def game_id_predicate(self):
        """
        Returns a selection of the game id.
        """
        return Game.select(Game.game_id)

    def populate_table(self, game_set, ignore_dups=False):
        """
        Takes a set of tuples and builds the game table.
        @params:
        game_set   - Required  : Set of GameEntry namedtuple entries (Set)
        ignore_dups - Optional : Will ignore duplicate entries if present.
        """
        rows = []

        for entry in game_set:
            # A bit of a hack. We shouldn't rely on data in requests
            # because it could change and invalidate this logic.
            away_team, home_team = entry.matchup_in.split(" @ ")

            try:
                new_row = {
                    'game_id': entry.game_id,
                    'team_id_home': team_abbrev_mapping[home_team],
                    'team_id_away': team_abbrev_mapping[away_team],
                    'season_id': entry.season_id,
                    'date': entry.game_date
                }
            except KeyError as e:
                # TODO Support these.
                print(f"Unsupported team abbreviation: {e.args[0]}")
                continue

            teams = [new_row['team_id_away'], new_row['team_id_home']]
            if entry.winner:
                new_row['team_id_winner'] = entry.winner
                new_row['team_id_loser'] = teams[teams.index(entry.winner) - 1]
            else:
                new_row['team_id_loser'] = entry.loser
                new_row['team_id_winner'] = teams[teams.index(entry.loser) - 1]

            rows.append(new_row)

        if ignore_dups:
            insert_many_on_conflict_ignore(self.settings, Game, rows)
        else:
            insert_many(self.settings, Game, rows)
