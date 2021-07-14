from peewee import (
    PostgresqlDatabase,
    MySQLDatabase
)

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

    def __init__(self, database):

        self.user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82"
            "Safari/537.36"
        )

        if database == "postgres":
            print("Connecting to postgres database.")
            self.db = PostgresqlDatabase(
                DB_NAME,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
        else:
            print("Connecting to mysql database.")
            self.db = MySQLDatabase(
                DB_NAME,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                charset='utf8mb4'
            )
