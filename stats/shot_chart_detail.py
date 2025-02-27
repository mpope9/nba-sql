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


ShotChartDetail builder and requester.
"""

import urllib.parse

from models import ShotChartDetail, ShotChartDetailTemp
from general_requester import GenericRequester
from db_utils import insert_many


class ShotChartDetailRequester(GenericRequester):

    shot_chart_detail_url = "https://stats.nba.com/stats/shotchartdetail"

    def __init__(self, settings):
        """
        Constructor. Pass on all relevant vars.
        """
        super().__init__(settings, self.shot_chart_detail_url, ShotChartDetail)
        # TODO: this conflicts with a fresh db.
        self.settings.db.bind([ShotChartDetailTemp])
        self.settings.db.create_tables([ShotChartDetailTemp], safe=True)

    def create_ddl(self):
        """
        Override method to setup temp table.
        """
        super().create_ddl()

    def temp_table_except_predicate(self):
        """
        This runs an EXCEPT between the temp table and the non-temp table to find
        the new games.

        This is a silly way to do this, but I wanted a quick copy/paste to unblock
        something else.
        """
        regular_query = ShotChartDetail.select(ShotChartDetail.game_id)
        temp_query = ShotChartDetailTemp.select(ShotChartDetailTemp.game_id)

        expt = temp_query - regular_query

        return expt.select_from(expt.c.game_id)

    def finalize(self, filter_predicate):
        """
        This function finishes loading shot_chart_detail by inserting all valid
        records from the temp table into the main table. The temp table is
        dropped at the end of the session.

        This accepts a predicate to define what game_ids to filter on.
        Examples of usage: to only add rows for existing games, or for the
        EXCEPT for the player_game_log regular and temp tables.
        """
        print('Inserting from shot_chart_detail temp table into main table.')
        with self.settings.db.atomic():
            (ShotChartDetail.insert_from(
                ShotChartDetailTemp.select(
                            ShotChartDetailTemp.game_id,
                            ShotChartDetailTemp.player_id,
                            ShotChartDetailTemp.team_id,
                            ShotChartDetailTemp.game_event_id,
                            ShotChartDetailTemp.period,
                            ShotChartDetailTemp.minutes_remaining,
                            ShotChartDetailTemp.seconds_remaining,
                            ShotChartDetailTemp.event_type,
                            ShotChartDetailTemp.action_type,
                            ShotChartDetailTemp.shot_type,
                            ShotChartDetailTemp.shot_zone_basic,
                            ShotChartDetailTemp.shot_zone_area,
                            ShotChartDetailTemp.shot_zone_range,
                            ShotChartDetailTemp.shot_distance,
                            ShotChartDetailTemp.loc_x,
                            ShotChartDetailTemp.loc_y,
                            ShotChartDetailTemp.shot_attempted_flag,
                            ShotChartDetailTemp.shot_made_flag,
                            ShotChartDetailTemp.htm,
                            ShotChartDetailTemp.vtm
                ).where(ShotChartDetailTemp.game_id.in_(filter_predicate)),
                # TODO: Cleaner way to specify all fields but one?
                fields=[
                    ShotChartDetail.game_id,
                    ShotChartDetail.player_id,
                    ShotChartDetail.team_id,
                    ShotChartDetail.game_event_id,
                    ShotChartDetail.period,
                    ShotChartDetail.minutes_remaining,
                    ShotChartDetail.seconds_remaining,
                    ShotChartDetail.event_type,
                    ShotChartDetail.action_type,
                    ShotChartDetail.shot_type,
                    ShotChartDetail.shot_zone_basic,
                    ShotChartDetail.shot_zone_area,
                    ShotChartDetail.shot_zone_range,
                    ShotChartDetail.shot_distance,
                    ShotChartDetail.loc_x,
                    ShotChartDetail.loc_y,
                    ShotChartDetail.shot_attempted_flag,
                    ShotChartDetail.shot_made_flag,
                    ShotChartDetail.htm,
                    ShotChartDetail.vtm
                ]
            )).execute()

        print('Insert finished.')

    def generate_rows(self, team_id, player_id):
        """
        Build GET REST request to the NBA for a season.
        """
        params = self.build_params(team_id, player_id)

        # Encode without safe '+', apparently the NBA likes unsafe url params.
        params_str = urllib.parse.urlencode(params, safe=':+')
        super().generate_rows(params_str)

    def populate(self):
        """
        Store collected rows. Custom implementation to clear out the rows beteen
        populations and insert into the staging table.
        """
        insert_many(self.settings, ShotChartDetailTemp, self.rows)
        self.rows = []

    def build_params(self, team_id, player_id):
        """
        Create required parameters dict for the request.
        """
        params = self.base_params()
        params['PlayerID'] = player_id
        params['TeamID'] = team_id
        return params

    def base_params(self):
        """
        The base params map.
        """
        return {
                'AheadBehind': '',
                'ClutchTime': '',
                'ContextFilter': '',
                'ContextMeasure': 'FGA',
                'DateFrom': '',
                'DateTo': '',
                'EndPeriod': '',
                'EndRange': '',
                'GameID': '',
                'GameSegment': '',
                'LastNGames': '0',
                'LeagueID': '00',
                'Location': '',
                'Month': '0',
                'OpponentTeamID': '0',
                'Outcome': '',
                'Period': '0',
                'PlayerID': '',
                'PlayerPosition': '',
                'PointDiff': '',
                'Position': '',
                'RangeType': '',
                'RookieYear': '',
                'Season': '',
                'SeasonSegment': '',
                'SeasonType': 'Regular+Season',
                'StartPeriod': '',
                'StartRange': '',
                'TeamID': '',
                'VsConference': '',
                'VsDivision': ''
        }
