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


Database utilities (future middleware layer if we decide to use DuckDB by default.)
"""

from utils import chunk_list


def insert_many(settings, table, rows):
    """
    Entry function on insert_many.
    """

    chunked_rows = chunk_list(rows, settings.batch_size)
    if settings.db_type == 'sqlite':
        __insert_many_sqlite(settings, table, rows)
    else:
        with settings.db.atomic():
            for row in chunked_rows:
                table.insert_many(row).execute()


def __insert_many_sqlite(settings, table, rows):
    """
    SQLite has a limit on number of rows. Chunk the rows and batch insert.
    """

    chunked_rows = chunk_list(rows, 500)
    with settings.db.atomic():
        for row in chunked_rows:
            table.insert_many(row).execute()


def insert_many_on_conflict_ignore(settings, table, rows):
    """
    Entry function on insert_many, ignoring conflicts on key issues.
    """

    if settings.db_type == 'sqlite':
        __insert_many_on_conflict_ignore_sqlite(settings, table, rows)
    else:
        with settings.db.atomic():
            table.insert_many(rows).on_conflict_ignore().execute()


def __insert_many_on_conflict_ignore_sqlite(settings, table, rows):
    """
    SQLite has a limit on number of rows. Chunk the rows and batch insert.
    """

    chunked_rows = chunk_list(rows, 500)
    with settings.db.atomic():
        for row in chunked_rows:
            table.insert_many(row).on_conflict_ignore().execute()
