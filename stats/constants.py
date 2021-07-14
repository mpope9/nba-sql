"""
Constants used in the application.
"""

"""
List of seasons.
"""
season_list = [
    '1996-97',
    '1997-98',
    '1998-99',
    '1999-00',
    '2000-01',
    '2001-02',
    '2002-03',
    '2003-04',
    '2004-05',
    '2005-06',
    '2006-07',
    '2007-08',
    '2008-09',
    '2009-10',
    '2010-11',
    '2011-12',
    '2012-13',
    '2013-14',
    '2014-15',
    '2015-16',
    '2016-17',
    '2017-18',
    '2018-19',
    '2019-20',
    '2020-21'
]

"""
Headers.
"""
headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130'
        'Safari/537.36'
    ),
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

"""
Team IDs. (Thank you nba-api).
"""
team_ids = [
    1610612737,     # 'ATL'
    1610612738,     # 'BOS'
    1610612739,     # 'CLE'
    1610612740,     # 'NOP'
    1610612741,     # 'CHI'
    1610612742,     # 'DAL'
    1610612743,     # 'DEN'
    1610612744,     # 'GSW'
    1610612745,     # 'HOU'
    1610612746,     # 'LAC'
    1610612747,     # 'LAL'
    1610612748,     # 'MIA'
    1610612749,     # 'MIL'
    1610612750,     # 'MIN'
    1610612751,     # 'BKN'
    1610612752,     # 'NYK'
    1610612753,     # 'ORL'
    1610612754,     # 'IND'
    1610612755,     # 'PHI'
    1610612756,     # 'PHX'
    1610612757,     # 'POR'
    1610612758,     # 'SAC'
    1610612759,     # 'SAS'
    1610612760,     # 'OKC'
    1610612761,     # 'TOR'
    1610612762,     # 'UTA'
    1610612763,     # 'MEM'
    1610612764,     # 'WAS'
    1610612765,     # 'DET'
    1610612766,     # 'CHA'
]

"""
Mapping from team abbrev to id.
"""
team_abbrev_mapping = {
    'ATL': 1610612737,
    'BOS': 1610612738,
    'CLE': 1610612739,
    'NOP': 1610612740,
    'NOK': 1610612740,  # Old name.
    'CHH': 1610612740,  # Old name.
    'NOH': 1610612740,  # Old name.
    'CHI': 1610612741,
    'DAL': 1610612742,
    'DEN': 1610612743,
    'GSW': 1610612744,
    'HOU': 1610612745,
    'LAC': 1610612746,
    'LAL': 1610612747,
    'MIA': 1610612748,
    'MIL': 1610612749,
    'MIN': 1610612750,
    'BKN': 1610612751,
    'NJN': 1610612751,  # Old name.
    'NYK': 1610612752,
    'ORL': 1610612753,
    'IND': 1610612754,
    'PHI': 1610612755,
    'PHX': 1610612756,
    'POR': 1610612757,
    'SAC': 1610612758,
    'SAS': 1610612759,
    'OKC': 1610612760,
    'SEA': 1610612760,
    'TOR': 1610612761,
    'UTA': 1610612762,
    'VAN': 1610612763,  # Old name.
    'MEM': 1610612763,
    'WAS': 1610612764,
    'DET': 1610612765,
    'CHA': 1610612766,
}


"""
Play-by-play data has an EventMsgType field. This is an enum. There
is also the EventMsgActionField, which is a complex enum of
(EventMsgType, SubType).
We're going to make a lookup table of enum to value, then a lookup
table for the (EventMsgType, EventMsgActionType) pair.
"""
event_message_types = [
    {'id': 1, 'string': 'FIELD_GOAL_MADE'},
    {'id': 2, 'string': 'FIELD_GOAL_MISSED'},
    {'id': 3, 'string': 'FREE_THROW'},
    {'id': 4, 'string': 'REBOUND'},
    {'id': 5, 'string': 'TURNOVER'},
    {'id': 6, 'string': 'FOUL'},
    {'id': 7, 'string': 'VIOLATION'},
    {'id': 8, 'string': 'SUBSTITUTION'},
    {'id': 9, 'string': 'TIMEOUT'},
    {'id': 10, 'string': 'JUMP_BALL'},
    {'id': 11, 'string': 'EJECTION'},
    {'id': 12, 'string': 'PERIOD_BEGIN'},
    {'id': 13, 'string': 'PERIOD_END'},
    {'id': 18, 'string': 'UNKNOWN'}
]
