from peewee import PostgresqlDatabase, MySQLDatabase, SqliteDatabase

import os
from dotenv import load_dotenv
load_dotenv()

"""
Singleton settings instance.
"""

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


class Settings:

    def __init__(self, database_type, database_name, database_user, database_password, database_host):

        self.user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82"
            "Safari/537.36"
        )

        self.db_type = database_type

        name = DB_NAME
        user = DB_USER
        password = DB_PASSWORD
        host = DB_HOST

        if database_name is not None:
            name = database_name
        if database_user is not None:
            user = database_user
        if database_password is not None:
            password = database_password
        if database_host is not None:
            host = database_host

        if database_type == "postgres":
            print("Connecting to postgres database.")
            self.db = PostgresqlDatabase(
                name,
                host=host,
                user=user,
                password=password
            )
        elif database_type == "sqlite":
            print("Initializing sqlite database.")
            self.db = SqliteDatabase('nba_sql.db', pragmas={'journal_mode': 'wal'})
        else:
            print("Connecting to mysql database.")
            self.db = MySQLDatabase(
                name,
                host=host,
                user=user,
                password=password,
                charset='utf8mb4'
            )
