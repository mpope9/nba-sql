from team import TeamRequester
from player import PlayerRequester
from event_message_type import EventMessageTypeBuilder
from game import GameBuilder

from player_season import PlayerSeasonRequester
from player_game_log import PlayerGameLogRequester
from player_general_traditional_total import (
    PlayerGeneralTraditionalTotalRequester
)
from play_by_play import PlayByPlayRequester
from shot_chart_detail import ShotChartDetailRequester

from constants import season_list, team_ids
from settings import Settings

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


def main():
    """
    Main driver for the nba_sql application.
    """

    parser = argparse.ArgumentParser(description=description)

    last_loadable_season = season_list[-1]

    parser.add_argument(
        '--seasons',
        dest='seasons',
        default=last_loadable_season,
        choices=season_list,
        help="""
            The seasons flag loads the database with the specified season.
            The format of the season should be in the form "YYYY-YY".
            The default behavior is loading the current season.
            Example usage:
            --seasons 2019-2020 2020-2021
            """
    )

    parser.add_argument(
        '--skip-base-tables',
        action="store_true",
        default=False,
        help="""
            Flag to skip loading the 'base' tables, which are player and team.
            Useful if one already has an initialized database and only
            wants to fill/update
            a season.
            """
    )

    parser.add_argument(
        '--create-schema',
        dest='create_schema',
        action="store_true",
        default=False,
        help="""
            Flag to initialize the database schema before loading data.
            """
    )

    parser.add_argument(
        '--database',
        dest='database',
        default='mysql',
        choices=['mysql', 'postgres', 'sqlite'],
        help="""
            The database flag specifies which database protocol to use.
            Defaults to "mysql", but also accepts "postgres" and "sqlite".
            Example usage:
            --database postgres
            """
    )

    parser.add_argument(
        '--time-between-requests',
        dest='request_gap',
        default='.7',
        help="""
            This flag exists to prevent rate limiting,
            and we inject a sleep inbetween requesting resources.
            """
    )

    parser.add_argument(
        '--skip-tables',
        action='store',
        nargs="*",
        default=[],
        choices=['player_season', 'player_game_log', 'play_by_play', 'pgtt', 'shot_chart_detail'],
        help=(
            "Use this option to skip loading certain tables. "
            " Example: --skip-tables play_by_play pgtt"
        ))

    args = parser.parse_args()

    # CMD line args.
    database = args.database
    create_schema = args.create_schema
    request_gap = float(args.request_gap)
    skip_base_tables = args.skip_base_tables
    seasons = []
    seasons.append(args.seasons)
    skip_tables = args.skip_tables

    settings = Settings(database)

    player_requester = PlayerRequester(settings)
    team_requester = TeamRequester(settings)
    event_message_type_builder = EventMessageTypeBuilder(settings)
    game_builder = GameBuilder(settings)

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

        # Dependent Objects
        player_season_requester,
        player_game_log_requester,
        play_by_play_requester,
        pgtt_requester,
        shot_chart_requester
    ]

    if create_schema:
        do_create_schema(object_list)

    if not skip_base_tables:
        populate_base_tables(
            seasons,
            request_gap,
            team_requester,
            player_requester,
            event_message_type_builder)

    player_game_seasons_bar = progress_bar(
        seasons,
        prefix='Loading player_game_log season Data',
        suffix='This one will take a while...',
        length=30)

    # Fetch player_game_log and build game_id set.
    for season_id in player_game_seasons_bar:

        player_game_log_requester.fetch_season(season_id)
        time.sleep(request_gap)

    # First, load game specific data.
    game_set = player_game_log_requester.get_game_set()
    print('Loading cached game table.')
    game_builder.populate_table(game_set)

    # Fetch ids from tuples.
    game_list = [game[1] for game in game_set]

    game_progress_bar = progress_bar(
        game_list,
        prefix='Loading PlayByPlay Data',
        length=30)

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

        shot_chart_requester.finalize()

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


def populate_base_tables(seasons, request_gap, team_requester, player_requester, event_message_type_builder):
    """
    Populates base tables.
    """
    print('Populating base tables')

    team_bar = progress_bar(team_ids, prefix='team Table Loading', suffix='', length=30)
    player_bar = progress_bar(seasons, prefix='player Table Loading', suffix='', length=30)

    # Load team data.
    print('Populating team data')
    for team_id in team_bar:
        team_requester.generate_rows(team_id)
        time.sleep(request_gap)
    team_requester.populate()

    # Load player data.
    print('Populating player data')
    for season_id in player_bar:
        player_requester.generate_rows(season_id)
        time.sleep(request_gap)
    player_requester.populate()

    print('Loading event types.')
    event_message_type_builder.initialize()


def progress_bar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = 1
    if iterable:
        total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = (
            ("{0:." + str(decimals) + "f}")
            .format(100 * (iteration / float(total)))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


if __name__ == "__main__":
    main()
