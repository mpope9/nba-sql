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


Class for user defined settings.
"""

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

    def __init__(self, database_type, database_name,
                 database_user, database_password, database_host,
                 batch_size, sqlite_path, quiet):

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
        self.batch_size = batch_size

        if database_name is not None:
            name = database_name
        if database_user is not None:
            user = database_user
        if database_password is not None:
            password = database_password
        if database_host is not None:
            host = database_host

        if database_type == "postgres":
            if not quiet:
                print("Connecting to postgres database.")
            self.db = PostgresqlDatabase(
                name,
                host=host,
                user=user,
                password=password
            )
        elif database_type == "sqlite":
            if not quiet:
                print("Initializing sqlite database.")
            self.db = SqliteDatabase(sqlite_path, pragmas={'journal_mode': 'wal'})
        else:
            if not quiet:
                print("Connecting to mysql database.")
            self.db = MySQLDatabase(
                name,
                host=host,
                user=user,
                password=password,
                charset='utf8mb4'
            )
