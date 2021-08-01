import urllib.parse
from models import Player
from general_requester import GenericRequester


class PlayerRequester(GenericRequester):

    per_mode = 'Totals'
    player_info_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats'

    def __init__(self, settings):
        """
        Constructor. Pass on all relevant vars.
        """
        super().__init__(settings, self.player_info_url, Player)

    def get_id_set(self):
        """
        Gets a set of ids for caching.
        """
        s = set()
        for player in Player.select(Player.player_id):
            s.add(player.player_id)
        return s

    def generate_rows(self, season_id):
        """
        Build GET REST request to the NBA for a season.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')
        super().generate_rows(params_str)

    def populate(self):
        """
        Store collected rows. Custom implementation for the on_conflict_ignore
        argument.
        """
        Player.insert_many(self.rows).on_conflict_ignore().execute()

    def build_params(self, season_id):
        """
        Create required parameters dict for the request.
        """
        return {
            'College': '',
            'Conference': '',
            'Country': '',
            'DateFrom': '',
            'DateTo': '',
            'Division': '',
            'DraftPick': '',
            'DraftYear': '',
            'GameScope': '',
            'GameSegment': '',
            'Height': '',
            'LastNGames': '0',
            'LeagueID': '00',
            'Location': '',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PerMode': self.per_mode,
            'Period': '0',
            'PlayerExperience': '',
            'PlayerPosition': '',
            'Season': season_id,
            'SeasonSegment': '',
            'SeasonType': 'Regular+Season',
            'ShotClockRange': '',
            'StarterBench': '',
            'TeamID': '0',
            'VsConference': '',
            'VsDivision': '',
            'Weight': ''
        }
