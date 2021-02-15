description = """
    nba_sql application.
    
    The command loads the database with historic data from the 1996-97 / 2019-20 seasons.
    EX:
        python3 stats/nba_sql.py
    """

from settings import Settings
import constants
import argparse

from models import PlayerGeneralTraditionalTotals
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

    if create_schema:
        do_create_schema(settings)

def do_create_schema(settings):
    """
    Function to initialize database schema.
    """
    print("Initializing schema.")

    settings.db.bind([PlayerBios, PlayerGameLogs, PlayerGeneralTraditionalTotals])
    settings.db.create_tables([PlayerBios], safe=True)
    settings.db.create_tables([PlayerGameLogs], safe=True)
    settings.db.create_tables([PlayerGeneralTraditionalTotals], safe=True)

if __name__ == "__main__":
    main()
