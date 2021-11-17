from utils import chunk_list


"""
Database utilities (future middleware layer if we decide to use DuckDB by default.)
"""


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
