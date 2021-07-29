"""
Misc utilities.
"""


def get_rowset_mapping(result_sets, column_names):
    """
    Returns a list of mapped fields to the passed headers.
    """

    headers = result_sets['headers']
    return {column: headers.index(column.upper()) for column in column_names}


def column_names_from_columns(db, table_name):
    """
    Gets the column names from a db table.
    """

    columns = db.get_columns(table_name)
    return [column.name for column in columns]
