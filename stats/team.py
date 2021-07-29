import requests
from utils import get_rowset_mapping, column_names_from_columns

from models import Team
from constants import headers


class TeamRequester:

    team_details_url = 'https://stats.nba.com/stats/teamdetails'
    rows = []

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        self.settings = settings
        self.settings.db.bind([Team])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([Team], safe=True)

    def add_team(self, team_id):
        """
        Build GET Request for the team id.
        Since we're in the context of a single team, we'll assemble rows
        one at a time then do a bulk insert at the end.
        """
        params = {'TeamID': team_id}

        # json response
        response = requests.get(url=self.team_details_url, headers=headers, params=params).json()

        result_sets = response['resultSets'][0]
        team_detail = result_sets['rowSet']

        column_names = column_names_from_columns(self.settings.db, 'team')

        column_mapping = get_rowset_mapping(result_sets, column_names)

        for row in team_detail:
            new_row = {column_name: row[row_index] for column_name, row_index in column_mapping.items()}
            self.rows.append(new_row)

    def populate(self):
        """
        Bulk insert teams.
        """
        Team.insert_many(self.rows).execute()
