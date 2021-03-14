#!/bin/bash

docker exec -i nba_sql_db psql -U nba_sql nba < scripts/drop.sql
