#!/bin/bash

COMMAND=docker
if command -v podman 2>&1 >/dev/null
then
  COMMAND=podman
fi
echo "Running command with $COMMAND"
$COMMAND exec -i nba_sql_db psql -U nba_sql nba < scripts/drop.sql
