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


Team requester and builder.
"""

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
