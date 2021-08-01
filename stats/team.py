from models import Team
from general_requester import GenericRequester


class TeamRequester(GenericRequester):

    team_details_url = 'https://stats.nba.com/stats/teamdetails'

    def __init__(self, settings):
        """
        Constructor. Pass on all relevant vars.
        """
        super().__init__(settings, self.team_details_url, Team)

    def generate_rows(self, team_id):
        """
        Build GET Request for the team id.
        """
        params = {'TeamID': team_id}
        super().generate_rows(params)
