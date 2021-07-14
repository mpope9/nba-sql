from models import Game
from constants import team_abbrev_mapping


class GameBuilder:

    def __init__(self, settings):
        self.settings = settings
        self.settings.db.bind([Game])

    def create_ddl(self):
        """
        Creates the game table from the model.
        """
        self.settings.db.create_tables([Game], safe=True)

    def populate_table(self, game_set):
        """
        Takes a set of tuples and builds the game table.
        """

        rows = []

        for item in game_set:
            season_id = item[0]
            game_id = item[1]
            game_date = item[2]
            matchup_in = item[3]

            # A bit of a hack. We shouldn't rely on data in requests
            # because it could change and invalidate this logic.
            split = matchup_in.split(" @ ")
            away_team = split[0]
            home_team = split[1]

            # TODO Support these.
            if home_team not in team_abbrev_mapping:
                print("Unsupported team abbreviation: %s" % home_team)
                continue

            if away_team not in team_abbrev_mapping:
                print("Unsupported team abbreviation: %s" % away_team)
                continue

            new_row = {
                'game_id': game_id,
                'team_id_home': team_abbrev_mapping[home_team],
                'team_id_away': team_abbrev_mapping[away_team],
                'season_id': season_id,
                'date': game_date
            }
            rows.append(new_row)

        Game.insert_many(rows).execute()
