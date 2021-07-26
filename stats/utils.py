"""
Misc utilities.
"""


def get_rowset_mapping(result_sets, required_fields):
    """
    Returns a list of mapped fields to the passed headers.
    """

    headers = result_sets['headers']
    return list(map(lambda field, headers=headers: headers.index(field), required_fields))
