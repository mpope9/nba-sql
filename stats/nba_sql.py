description = """
    nba_sql application.
    
    The command loads the database with historic data from the 1996-97 / 2019-20 seasons.
    EX:
        python3 stats/nba_sql.py
    """

from constants import season_list, team_ids
from settings import Settings
import concurrent.futures
import argparse
import time
import copy

from team import TeamRequester
from player import PlayerRequester
from event_message_type import EventMessageTypeBuilder
from game import GameBuilder

from player_season import PlayerSeasonRequester
from player_game_log import PlayerGameLogRequester
from player_general_traditional_total import PlayerGeneralTraditionalTotalRequester
from play_by_play import PlayByPlayRequester

def main():
    """
    Main driver for the nba_sql application.
    """

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--season', dest='season', default='all', 
        help="""
            The season flag loads the database with the specified season. 
            The format of the season should be in the form "YYYY-YY".
            """)

    parser.add_argument('--base_tables', dest='do_base_tables', default=True,
        help="""
            Flag to designate filling the 'base' tables, which are player and team.
            Useful if one already has an initialized database and only wants to fill/update
            a season.
            """)

    parser.add_argument('--create_schema', dest='create_schema', default=False, 
        help="""
            The create_schema flag is used to initialize the database schema before loading data.
            """)

    parser.add_argument('--database', dest='database', default='mysql', 
        help="""
            The dtatbase flag specifies which database protocol to use. 
            Defaults to "mysql", but also accepts "postgres".
            """)

    parser.add_argument('--time_between_requests', dest='request_gap', default='.5',
        help="""
            This flag exists to prevent rate limiting, and we inject a sleep inbetween requesting
            resources.
            """)

    args = parser.parse_args()

    ## CMD line args.
    database = args.database
    create_schema = args.create_schema
    request_gap = float(args.request_gap)
    do_base_tables = args.do_base_tables
    season = args.season

    seasons = []
    if season is not None:
        seasons.append(season)
    else:
        seasons = season_list

    settings = Settings(database)

    player_requester = PlayerRequester(settings)
    team_requester = TeamRequester(settings)
    event_message_type_builder = EventMessageTypeBuilder(settings)
    game_builder = GameBuilder(settings)

    player_season_requester = PlayerSeasonRequester(settings)
    player_game_log_requester = PlayerGameLogRequester(settings)
    pgtt_requester = PlayerGeneralTraditionalTotalRequester(settings)
    play_by_play_requester = PlayByPlayRequester(settings)

    object_list = [
        # Base Objects
        player_requester,
        team_requester,
        event_message_type_builder,
        game_builder,

        ## Dependent Objects
        player_season_requester,
        player_game_log_requester,
        play_by_play_requester,
        pgtt_requester
    ]
    do_create_schema(create_schema, object_list)

    populate_base_tables(
        do_base_tables,
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

    player_game_log_rows = []
    # Fetch player_game_log and build game_id set.
    for season_id in player_game_seasons_bar:

        player_game_log_requester.fetch_season(season_id)
        time.sleep(request_gap)

    ## First, load game specific data.
    game_set = player_game_log_requester.get_game_set()
    print('Loading cached game table.')
    game_builder.populate_table(game_set)

    game_list = [game[1] for game in game_set] ## Fetch ids from tuples.
    game_progress_bar = progress_bar(
        game_list, 
        prefix='Loading PlayByPlay Data',
        length=30)

    ## Load game dependent data.
    player_id_set = player_requester.get_id_set()
    rows = []

    ## Okay so this takes a really long time due to rate limiting and over 25K games.
    ## Best we can do so far is batch the rows into groups of 100K and insert them in a
    ## different thread.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for game_id in game_progress_bar:
            new_rows = play_by_play_requester.fetch_game(game_id)
            rows += new_rows

            if len(rows) > 100000:
                ## We should be good for the race condition here.
                ## It takes a wee bit to insert 100K rows.
                copy_list = copy.deepcopy(rows)
                executor.submit(play_by_play_requester.insert_batch, copy_list, player_id_set)
                rows = []
            time.sleep(request_gap)

    ## Finally store player_game_log data after loading came data.
    print("Storing player_game_log table.")
    player_game_log_requester.store_rows()

    season_bar = progress_bar(
        seasons,
        prefix='Loading Seasonal Data',
        suffix='This one will take a while...',
        length=30)

    ## Load seasonal data.
    for season_id in player_game_seasons_bar:

        player_season_requester.populate_season(season_id)
        time.sleep(request_gap)

        pgtt_requester.populate_season(season_id)
        time.sleep(request_gap)

    print("Done! Enjoy the hot, fresh database.")

def do_create_schema(create_schema, object_list):
    """
    Function to initialize database schema.
    """
    if not create_schema:
        return

    print("Initializing schema.")

    for obj in object_list:
        obj.create_ddl()

def populate_base_tables(do_base_tables, seasons, request_gap, team_requester, player_requester, 
    event_message_type_builder):
    """
    Populates base tables.
    """

    if not do_base_tables:
        return

    team_bar = progress_bar(
        team_ids, 
        prefix='team Table Loading', 
        suffix='', 
        length=30)

    player_bar = progress_bar(
        seasons, 
        prefix='player Table Loading',
        suffix='',
        length=30)

    # Load team data.
    print('Populating team data')
    for team_id in team_bar:
        team_requester.add_team(team_id)
        time.sleep(request_gap)
    team_requester.populate()

    # Load player data.
    print('Populating player data')
    for season_id in player_bar:
        player_requester.add_player(season_id)
        time.sleep(request_gap)
    player_requester.populate()

    print('Loading event types.')
    event_message_type_builder.initialize()

def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = 1
    if iterable:
        total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
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
