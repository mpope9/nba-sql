import requests
import urllib.parse

from models import PlayerGeneralTraditionalTotal
from constants import headers


class PlayerGeneralTraditionalTotalRequester:

    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats'
    per_mode = 'Totals'

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        self.settings = settings
        self.settings.db.bind([PlayerGeneralTraditionalTotal])

    def create_ddl(self):
        """
        Initialize the table schema.
        """
        self.settings.db.create_tables(
            [PlayerGeneralTraditionalTotal],
            safe=True
        )

    def populate_season(self, season_id):
        """
        Build GET REST request to the NBA for a season,
        iterate over the results, store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')
        response = (
            requests
            .get(url=self.player_info_url, headers=headers, params=params_str)
            .json()
        )

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        rows = []

        for row in player_info:
            new_row = {
                'season_id': int(season_id[:4]),
                'player_id': row[0],
                'team_id': row[3],
                'age': row[5],
                'gp': row[6],
                'w': row[7],
                'l': row[8],
                'w_pct': row[9],
                'min': row[10],
                'fgm': row[11],
                'fga': row[12],
                'fg_pct': row[13],
                'fg3m': row[14],
                'fg3a': row[15],
                'fg3_pct': row[16],
                'ftm': row[17],
                'fta': row[18],
                'ft_pct': row[19],
                'oreb': row[20],
                'dreb': row[21],
                'reb': row[22],
                'ast': row[23],
                'tov': row[24],
                'stl': row[25],
                'blk': row[26],
                'blka': row[27],
                'pf': row[28],
                'pfd': row[29],
                'pts': row[30],
                'plus_minus': row[31],
                'nba_fantasy_pts': row[32],
                'dd2': row[33],
                'td3': row[34],
                'gp_rank': row[35],
                'w_rank': row[36],
                'l_rank': row[37],
                'w_pct_rank': row[38],
                'min_rank': row[39],
                'fgm_rank': row[40],
                'fga_rank': row[41],
                'fg_pct_rank': row[42],
                'fg3m_rank': row[43],
                'fg3a_rank': row[44],
                'fg3_pct_rank': row[45],
                'ftm_rank': row[46],
                'fta_rank': row[47],
                'ft_pct_rank': row[48],
                'oreb_rank': row[49],
                'dreb_rank': row[50],
                'reb_rank': row[51],
                'ast_rank': row[52],
                'tov_rank': row[53],
                'stl_rank': row[54],
                'blk_rank': row[55],
                'blka_rank': row[56],
                'pf_rank': row[57],
                'pfd_rank': row[58],
                'pts_rank': row[59],
                'plus_minus_rank': row[60],
                'nba_fantasy_pts_rank': row[61],
                'dd2_rank': row[62],
                'td3_rank': row[63],
                'cfid': row[64],
                'cfparams': row[65]
            }
            rows.append(new_row)
        PlayerGeneralTraditionalTotal.insert_many(rows).execute()

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
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PaceAdjust': 'N',
            'PerMode': self.per_mode,
            'Period': '0',
            'PlayerExperience': '',
            'PlayerPosition': '',
            'PlusMinus': 'N',
            'Rank': 'N',
            'Season': season_id,
            'SeasonSegment': '',
            'SeasonType': 'Regular+Season',
            'ShotClockRange': '',
            'StarterBench': '',
            'TeamID': '0',
            'TwoWay': '0',
            'VsConference': '',
            'VsDivision': '',
            'Weight': ''
        }
