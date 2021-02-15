import requests
import urllib.parse

from models import PlayerGeneralTraditionalTotals
from constants import season_list, headers

class PlayerGeneralTraditionalTotalsRequester:

    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats'
    per_mode = 'Totals'

    def __init__(self, settings):
        """
        Constructor. Attach settings internally and bind the model to the
        database.
        """
        self.settings = settings
        self.settings.db.bind([PlayerGeneralTraditionalTotals])

    def create(self):
        """
        Initialize the table schema.
        """
        settings.db.create_tables([PlayerGeneralTraditionalTotals], safe=True)

    def populate_season(self, season_id):
        """
        Build GET REST request to the NBA for a season, iterate over the results,
        store in the database.
        """
        params = self.build_params(season_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')
        response = requests.get(url=self.player_info_url, headers=headers, params=params_str).json()

        # pulling just the data we want
        player_info = response['resultSets'][0]['rowSet']

        for row in player_info:
            player = PlayerGeneralTraditionalTotals(
                season_id=season_id, # this is key, need this to join and sort by seasons
                player_id=row[0],
                player_name=row[1],
                team_id=row[2],
                team_abbreviation=row[3],
                age=row[4],
                gp=row[5],
                w=row[6],
                l=row[7],
                w_pct=row[8],
                min=row[9],
                fgm=row[10],
                fga=row[11],
                fg_pct=row[12],
                fg3m=row[13],
                fg3a=row[14],
                fg3_pct=row[15],
                ftm=row[16],
                fta=row[17],
                ft_pct=row[18],
                oreb=row[19],
                dreb=row[20],
                reb=row[21],
                ast=row[22],
                tov=row[23],
                stl=row[24],
                blk=row[25],
                blka=row[26],
                pf=row[27],
                pfd=row[28],
                pts=row[29],
                plus_minus=row[30],
                nba_fantasy_pts=row[31],
                dd2=row[32],
                td3=row[33],
                gp_rank=row[34],
                w_rank=row[35],
                l_rank=row[36],
                w_pct_rank=row[37],
                min_rank=row[38],
                fgm_rank=row[39],
                fga_rank=row[40],
                fg_pct_rank=row[41],
                fg3m_rank=row[42],
                fg3a_rank=row[43],
                fg3_pct_rank=row[44],
                ftm_rank=row[45],
                fta_rank=row[46],
                ft_pct_rank=row[47],
                oreb_rank=row[48],
                dreb_rank=row[49],
                reb_rank=row[50],
                ast_rank=row[51],
                tov_rank=row[52],
                stl_rank=row[53],
                blk_rank=row[54],
                blka_rank=row[55],
                pf_rank=row[56],
                pfd_rank=row[57],
                pts_rank=row[58],
                plus_minus_rank=row[59],
                nba_fantasy_pts_rank=row[60],
                dd2_rank=row[61],
                td3_rank=row[62],
                cfid=row[63],
                cfparams=row[64])
            player.save()

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
