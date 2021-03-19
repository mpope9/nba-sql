import requests
import urllib.parse

from settings import Settings
from models import Player
from constants import season_list, headers

class PlayerRequester:

    per_mode = 'Totals'
    player_info_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats'
    rows = []

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        self.settings = settings
        self.settings.db.bind([Player])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables([Player], safe=True)

    def get_id_set(self):
        """
        Gets a set of ids for caching.
        """
        s = set()
        for player in Player.select(Player.player_id):
            s.add(player.player_id)
        return s

    def add_player(self, season_id):
        """
        Build GET REST request to the NBA for a season.
        Since we're in the context of a single player, we'll assemble rows one at a time
        then do a bulk insert at the end.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')

	    # json response
        response = requests.get(url=self.player_info_url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        # looping over data to insert into table
        # direct array is a PITA, how can we abstract this...
        for row in player_info:
            new_row = {
                'player_id': row[0],
                'player_name': row[1],
                'college': row[8],
                'country': row[9],
                'draft_year': row[10],
                'draft_round': row[11],
                'draft_number': row[12]
            }
            self.rows.append(new_row)

    def populate(self):
        """
        Store collected rows.
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
