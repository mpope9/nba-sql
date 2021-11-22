#!/bin/bash

DB_NAME="nba" DB_HOST="localhost" DB_USER=nba_sql DB_PASSWORD=nba_sql python stats/nba_sql.py --default_mode --database="postgres" --skip-tables play_by_play pgtt
