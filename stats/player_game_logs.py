# player_bios.py - scraps data from stats.nba.com and inserts into player_bios table within MySQL nba stats database
import requests

from settings import Settings
from models import PlayerGameLogs

# TODO: Remove
settings = Settings()
settings.db.create_tables([PlayerGameLogs], safe=True)

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

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
	'2019-20'
]

#per_mode = 'Per100Possessions'
per_mode = 'Totals'
#per_mode = 'Per36'
#per_mode = 'PerGame'

# for loop to loop over seasons
for season_id in season_list:
    print("Now working on "+season_id+ " season")
    player_info_url = 'https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam='+type_player+'&Season='+season_id+'&SeasonType=Regular+Season&Sorter=DATE'
    # json response
    response = requests.get(url=player_info_url, headers=headers).json()
    # pulling just the data we want
    player_info = response['resultSets'][0]['rowSet']
    # looping over data to insert into table
    for row in player_info:
        player = PlayerGameLogs(
            season_id=season_id,  # this is key, need this to join and sort by seasons
            player_id=row[1],
            player_name=row[2],
            team_id=row[3],
            team_abbreviation=row[4],
            team_name=row[5],
            game_id=row[6],
            game_date=row[7],        
            matchup=row[8],
            wl=row[9],
            min=row[10],
            fgm=row[11],
            fga=row[12],
            fg_pct=row[13],
            fg3m=row[14],
            fg3a=row[15],
            fg3_pct=row[16],
            ftm=row[17],
            fta=row[18],
            ft_pct=row[19],
            oreb=row[20],
            dreb=row[21],
            reb=row[22],
            ast=row[23],
            stl=row[24],
            blk=row[25],
            tov=row[26],
            pf=row[27],
            pts=row[28],
            plus_minus=row[29],
            video_available=row[30]
            )
        player.save()

print ("Done inserting player bios data to the database!")
