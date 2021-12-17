from gooey import GooeyParser
from utils import generate_valid_seasons

"""
Creates a parser.
"""


def create_parser():
    """
    Creates and returns a Gooey parser.
    """

    parser = GooeyParser(description="nba-sql")

    mode_parser = parser.add_mutually_exclusive_group(
        required=True,
        gooey_options={
            'initial_selection': 0
        })
    mode_parser.add_argument(
        '--default_mode',
        help='Mode to create the database and load historic data. Use this mode when creating a new database or when trying to load a specific season or a range of seasons.',
        action='store_true')
    mode_parser.add_argument(
        '--current_season_mode',
        help='Mode to refresh the current season. Use this mode on an existing database to update it with the latest data.',
        action='store_true')

    parser.add_argument(
        '--database',
        dest='database_type',
        default='sqlite',
        choices=['mysql', 'postgres', 'sqlite'],
        help='The database flag specifies which database protocol to use.  Defaults to "sqlite", but also accepts "postgres" and "mysql".')

    parser.add_argument(
        '--database_name', 
        help="Database Name (Not Needed For SQLite)",
        default='nba')

    parser.add_argument(
        '--database_host', 
        help="Database Hostname (Not Needed For SQLite)",
        default=None)

    parser.add_argument(
        '--username',
        help="Database Username (Not Needed For SQLite)",
        default=None)

    parser.add_argument(
        '--password',
        help="Database Password (Not Needed For SQLite)",
        widget='PasswordField',
        default=None)

    valid_seasons = generate_valid_seasons()
    last_loadable_season = valid_seasons[-1]

    parser.add_argument(
        '--seasons',
        dest='seasons',
        default=[last_loadable_season],
        choices=valid_seasons,
        widget='Listbox',
        nargs="*",
        help='The seasons flag loads the database with the specified season.  The format of the season should be in the form "YYYY-YY".  The default behavior is loading the current season.')

    parser.add_argument(
        '--create-schema',
        dest='create_schema',
        action="store_true",
        default=True,
        help='Flag to initialize the database schema before loading data. If the schema already exists then nothing will happen.')

    parser.add_argument(
        '--time-between-requests',
        dest='request_gap',
        default='.7',
        help='This flag exists to prevent rate limiting, and injects the desired amount of time inbetween requesting resources.')

    parser.add_argument(
        '--skip-tables',
        action='store',
        nargs="*",
        default='',
        choices=['player_season', 'player_game_log', 'play_by_play', 'pgtt', 'shot_chart_detail', 'game', 'event_message_type', 'team', 'player', ''],
        widget='Listbox',
        help='Use this option to skip loading certain tables.')

    #To fix issue https://github.com/mpope9/nba-sql/issues/56
    parser.add_argument(
        '--batch_size',
        default='10000',
        type=int,
        help="Inserts BATCH_SIZE chunks of rows to the database. This value is ignored when selecting database 'sqlite'.")

    parser.add_argument(
        '--sqlite-path',
        dest='sqlite_path',
        default='nba_sql.db',
        help='Setting to define sqlite path.')

    parser.add_argument(
        '--quiet',
        dest='quiet',
        action='store_true',
        help='Setting to define stdout logging level. If set, only "ok" will be printed if ran successfully. This currently only applies to refreshing a db, and not loading one.')

    return parser
