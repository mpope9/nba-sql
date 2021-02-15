description = """
    nba_sql application.
    
    The command loads the database with historic data from the 1996-97 / 2019-20 seasons.
    EX:
        python3 stats/nba_sql.py
    """

from settings import Settings
from constants import season_list
import argparse

from player_general_traditional_totals import PlayerGeneralTraditionalTotalsRequester

from models import PlayerGameLogs
from models import PlayerBios

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

    parser.add_argument('--create_schema', dest='create_schema', default=False, 
        help="""
            The create_schema flag is used to initialize the database schema before loading data.
            """)

    parser.add_argument('--database', dest='database', default='mysql', 
        help="""
            The dtatbase flag specifies which database protocol to use. 
            Defaults to "mysql", but also accepts "postgres".
            """)

    args = parser.parse_args()

    database = args.database
    create_schema = args.create_schema

    settings = Settings(database)

    #player_bio_requester = PlayerBois(settings)
    pgtt_requester = PlayerGeneralTraditionalTotalsRequester(settings)

    if create_schema:
        do_create_schema(settings, pgtt_requester)

    # TODO: Limit seasons with the flag.
    for season_id in season_list:
        print("Populating season: %s" % (season_id))
        #player_bio_requester.populate_season(season_id)
        pgtt_requester.populate_season(season_id)

def do_create_schema(settings, pgtt_requester):
    """
    Function to initialize database schema.
    """
    print("Initializing schema.")

    settings.db.create_tables([PlayerBios], safe=True)
    settings.db.create_tables([PlayerGameLogs], safe=True)
    pgtt_requester.create()

if __name__ == "__main__":
    main()
