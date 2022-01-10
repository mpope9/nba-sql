from team import TeamRequester
from player import PlayerRequester
from event_message_type import EventMessageTypeBuilder
from game import GameBuilder
from season import SeasonBuilder

from player_season import PlayerSeasonRequester
from player_game_log import PlayerGameLogRequester
from player_general_traditional_total import (
    PlayerGeneralTraditionalTotalRequester
)
from play_by_play import PlayByPlayRequester
from shot_chart_detail import ShotChartDetailRequester

from constants import season_list, team_ids
from settings import Settings
from utils import progress_bar, generate_valid_seasons

from args import create_parser

import concurrent.futures
import argparse
import time
import copy

description = """
    nba_sql application.

    The command loads the database with historic data from the
    1996-97 / 2019-20 seasons.

    EX:
        python3 stats/nba_sql.py
    """

# TODO: load these args into the settings class.
def default_mode(settings, create_schema, request_gap, seasons, skip_tables):
    """
    The default mode of loading data. This is for initializing the database
    and loading specific seasons.
    """

    print("Loading the database in the default mode.")

    player_requester = PlayerRequester(settings)
    team_requester = TeamRequester(settings)
    event_message_type_builder = EventMessageTypeBuilder(settings)
    game_builder = GameBuilder(settings)
    season_builder = SeasonBuilder(settings)

    player_season_requester = PlayerSeasonRequester(settings)
    player_game_log_requester = PlayerGameLogRequester(settings)
    pgtt_requester = PlayerGeneralTraditionalTotalRequester(settings)
    play_by_play_requester = PlayByPlayRequester(settings)
    shot_chart_requester = ShotChartDetailRequester(settings)

    object_list = [
        # Base Objects
        player_requester,
        team_requester,
        event_message_type_builder,
        game_builder,
        season_builder,

        # Dependent Objects
        player_season_requester,
        player_game_log_requester,
        play_by_play_requester,
        pgtt_requester,
        shot_chart_requester
    ]

    if create_schema:
        do_create_schema(object_list)

    season_builder.populate(seasons)

    if 'team' not in skip_tables:
        print('Populating team table.')

        team_bar = progress_bar(team_ids, prefix='team Table Loading', suffix='', length=30)
        for team_id in team_bar:
            team_requester.generate_rows(team_id)
            time.sleep(request_gap)

        team_requester.populate()

    if 'event_message_type' not in skip_tables:
        print('Loading event types.')
        event_message_type_builder.initialize()

    if 'player' not in skip_tables:
        print('Populating player data')

        player_bar = progress_bar(seasons, prefix='player Table Loading', suffix='', length=30)
        for season_id in player_bar:
            player_requester.generate_rows(season_id)
            time.sleep(request_gap)
        player_requester.populate()

    player_game_seasons_bar = progress_bar(
        seasons,
        prefix='Loading player_game_log season Data',
        suffix='This one will take a while...',
        length=30)

    # Fetch player_game_log and build game_id set.
    for season_id in player_game_seasons_bar:

        player_game_log_requester.fetch_season(season_id)
        time.sleep(request_gap)

    game_set = player_game_log_requester.get_game_set()

    # Fetch ids from tuples.
    game_list = [game[1] for game in game_set]

    game_progress_bar = progress_bar(
        game_list,
        prefix='Loading PlayByPlay Data',
        length=30)

    # First, load game specific data.
    if 'game' not in skip_tables:
        print('Loading cached game table.')
        game_builder.populate_table(game_set)

    if 'play_by_play' not in skip_tables:
        # Load game dependent data.
        player_id_set = player_requester.get_id_set()
        rows = []

        # Okay so this takes a really long time due to rate
        # limiting and over 25K games. Best we can do so
        # far is batch the rows into groups of 100K and insert them
        # in a different thread.
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            for game_id in game_progress_bar:
                new_rows = play_by_play_requester.fetch_game(game_id)
                rows += new_rows

                if len(rows) > 100000:
                    # We should be good for the race condition here.
                    # It takes a wee bit to insert 100K rows.
                    copy_list = copy.deepcopy(rows)
                    executor.submit(
                        play_by_play_requester.insert_batch,
                        copy_list, player_id_set
                    )
                    rows = []
                time.sleep(request_gap)

    if 'player_game_log' not in skip_tables:

        print("Starting PlayerGameLog Insert")
        player_game_log_requester.populate()
        print("Finished PlayerGameLog Insert")

    if 'shot_chart_detail' not in skip_tables:

        print("Fetching set of team_id and player_ids for the ShotChartData.")
        team_player_set = player_game_log_requester.get_team_player_id_set()
        print("Finished fetching.")
        shot_chart_bar = progress_bar(
            team_player_set,
            prefix='Loading Shot Chart Data',
            suffix='',
            length=30)

        for id_tuple in shot_chart_bar:

            shot_chart_requester.generate_rows(id_tuple[0], id_tuple[1])
            shot_chart_requester.populate()
            time.sleep(request_gap)

        shot_chart_requester.finalize(game_builder.game_id_predicate())

    season_bar = progress_bar(
        seasons,
        prefix='Loading Seasonal Data',
        suffix='This one will take a while...',
        length=30)

    # Load seasonal data.
    for season_id in season_bar:
        if 'player_season' not in skip_tables:
            player_season_requester.populate_season(season_id)
            time.sleep(request_gap)

        if 'pgtt' not in skip_tables:
            pgtt_requester.generate_rows(season_id)
            time.sleep(request_gap)

    print("Done! Enjoy the hot, fresh database.")


def do_create_schema(object_list):
    """
    Function to initialize database schema.
    """
    print("Initializing schema.")

    for obj in object_list:
        obj.create_ddl()


def current_season_mode(settings, request_gap, skip_tables, quiet):
    """
    Refreshes the current season in a previously existing database.
    """

    if not quiet:
        print("Refreshing the current season in the existing database.")


    player_game_log_requester = PlayerGameLogRequester(settings)
    game_builder = GameBuilder(settings)
    shot_chart_requester = ShotChartDetailRequester(settings)
    season_builder = SeasonBuilder(settings)

    season_id = season_builder.current_season_loaded()
    season = generate_valid_season(season_id)

    if not quiet:
        print("Fetching current season data.")

    player_game_log_requester.fetch_season(season)
    player_game_log_requester.populate_temp()
    time.sleep(request_gap)

    if 'player_game_log' not in skip_tables:
        player_game_log_requester.insert_from_temp_into_reg()

    game_set = player_game_log_requester.get_game_set()
    # Insert new games and ignore duplicates, becuase its difficult to
    # do this the correct way.
    game_builder.populate_table(game_set, True)

    if 'shot_chart_detail' not in skip_tables:
        team_player_set = player_game_log_requester.get_team_player_id_set(True)

        shot_chart_bar = progress_bar(
            team_player_set,
            prefix='Loading Shot Chart Data',
            suffix='',
            length=30,
            quiet=quiet)

        for id_tuple in shot_chart_bar:

            shot_chart_requester.generate_rows(id_tuple[0], id_tuple[1])
            shot_chart_requester.populate()
            time.sleep(request_gap)

        scd_predicate = player_game_log_requester.temp_table_except_predicate()
        shot_chart_requester.finalize(scd_predicate)

    if quiet:
        print("ok")


def main(args):
    """
    Main driver for the nba-sql application.
    """

    # CMD line args.
    default_mode_set = args.default_mode
    current_season_mode_set = args.current_season_mode

    create_schema = args.create_schema
    request_gap = float(args.request_gap)
    seasons = args.seasons
    skip_tables = args.skip_tables
    quiet = args.quiet

    if not quiet:
        print(f"Loading seasons: {seasons}.")

    settings = Settings(
        args.database_type, 
        args.database_name, 
        args.username, 
        args.password,
        args.database_host,
        args.batch_size,
        args.sqlite_path,
        args.quiet)

    if default_mode_set:
        default_mode(settings, create_schema, request_gap, seasons, skip_tables)
    if current_season_mode_set:
        current_season_mode(settings, request_gap, skip_tables, quiet)


# Default non-gui executable.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='nba-sql')
    create_parser(parser)

    parser.add_argument(
        '--default-mode',
        help='Mode to create the database and load historic data. Use this mode when creating a new database or when trying to load a specific season or a range of seasons.',
        action='store_true')
    parser.add_argument(
        '--current-season-mode',
        help='Mode to refresh the current season. Use this mode on an existing database to update it with the latest data.',
        action='store_true')

    parser.add_argument(
        '--password',
        help="Database Password (Not Needed For SQLite)",
        default=None)

    valid_seasons = generate_valid_seasons()
    last_loadable_season = valid_seasons[-1]

    parser.add_argument(
        '--seasons',
        dest='seasons',
        default=[last_loadable_season],
        choices=valid_seasons,
        nargs="*",
        help='The seasons flag loads the database with the specified season.  The format of the season should be in the form "YYYY-YY".  The default behavior is loading the current season.')

    parser.add_argument(
        '--skip-tables',
        action='store',
        nargs="*",
        default='',
        choices=['player_season', 'player_game_log', 'play_by_play', 'pgtt', 'shot_chart_detail', 'game', 'event_message_type', 'team', 'player', ''],
        help='Use this option to skip loading certain tables.')

    args = parser.parse_args()

    main(args)
