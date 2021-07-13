# :basketball: nba-sql

[![Github All Releases](https://img.shields.io/github/downloads/mpope9/nba-sql/total.svg)]()

An application to build a Postgres or MySQL NBA database from the public API.

To access the latest Postgres dump file [check the releases tab](https://github.com/mpope9/nba-sql/releases).

To use a PG dump from the releases, decompress using `xc`, then load with `psql`, like this:
```bash
xz -d nba.sql.xz
psql -U <USERNAME> <DBNAME> < nba.sql
```

This DB is still under construction and liable to schema changes. v0.1.0 will be the final schema. Until then, expect to rebuild the whole DB when trying to upgrade.

The default behavior is collecting seasons 1996-97 to 2020-21 and inserting them into a MySQL database. There are flags provided to change to a Postgres database, and to specify a specific season. See commandline reference below.

Big shoutout to BurntSushi's [nfldb](https://github.com/BurntSushi/nfldb) as well as the [nba_api project](https://github.com/swar/nba_api). They are great inspirations and indispensable resources to this project.

# Getting Started

* [A good place for more information is the wiki](https://github.com/mpope9/nba-sql/wiki).
* [Looking to contribute? Check the list of open issues!](https://github.com/mpope9/nba-sql/issues)

It will take an estimated 3 hours to build the whole database. Around 10 mins if play-by-play data isn't desired.

The following environment variables must be set. There are no commandline arguments to specify these. The following example are connection details for the provided docker-compose database:
```
DB_NAME="nba"
DB_HOST="localhost"
DB_USER="nba_sql"
DB_PASSWORD="nba_sql"
```

Here is an example query which can be used after building the database. Lets say we want to find Russell Westbrook's total Triple-Doubles:
```
SELECT SUM(td3) 
FROM player_game_log 
LEFT JOIN player ON player.player_id = player_game_log.player_id 
WHERE player.player_name = 'Russell Westbrook';
```

## :crystal_ball: Schema
#### Supported Tables
* player
* team
* game
* play_by_play
* player_game_log
* player_season
* team_game_log
* team_season
* player_general_traditional_total (Also referred to in short as pgtt)

An up-to-date ER diagram can be found in [`image/NBA-ER.jpg`](https://github.com/mpope9/nba-sql/blob/master/image/NBA-ER.jpg).

## :wrench: Building From Scratch

Requirements:

Python >= 3.6

### :scroll: Provided Scripts

In the `scripts` directory, we provide a way to create the schema and load the data for a Postgres database. We also provide a docker-compose setup for development and to preview the data.

```shell
# Required if you're on Debian based systems
sudo service postgresql stop
docker-compose up -d

pip install -r requirements.txt

./scripts/create_postgres.sh
```

### :snake: Directly Calling Python

The entrypoint is `stats/nba_sql.py`. To see the available arguments, you can use:
```bash
python stats/nba_sql.py -h
```

To create the schema, use the `--create-schema`. Example:
```bash
pyhton stats/nba_sql.py --create-schema
```

To enable a Postgres database, use the `--database` flag. Example:
```bash
python stats/nba_sql.py --database="postgres"
```

We have added a half second delay between making requests to the NBA stats API. To configure the amount of time use the `--time-between-requests` flag.
```bash
python stats/nba_sql.py --time-between-requests=.5
```

The script `nba_sql.py` adds several tables into the database. Loading these tables takes time, notably, the `play_by_play` table. 
Some of these tables can be skipped by using the `--skip-tables` CLI option. Example:

```bash
python stats/nba_sq.py --create-schema --database postgres --skip-tables play_by_play pgtt
```

### :computer: Local development

##### The manual way
Create your virtual environment if you don’t have one already. In this case we use `venv` as the target folder for storing packages.

`python -m venv venv`

Then activate it:
`source venv/bin/activate`

Install dependencies using:
`pip install -r requirements.txt`
