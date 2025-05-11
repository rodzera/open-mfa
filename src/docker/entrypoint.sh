#!/usr/bin/env bash

DB_STATUS=1

while [[ $DB_STATUS -ne 0 ]] ; do
  sleep 2
  echo "Connecting into redis"
  DB_STATUS=$(python3 redis_conn.py)
done

echo "Redis connected"

if [[ "$DEBUG" -eq 1 || "$_DEBUG" -eq 1 || "$FLASK_DEBUG" -eq 1 ]]; then

  echo "Starting development server"
  flask --app run --debug run -h $HOST -p $PORT

else

  echo "Starting production server"
  gunicorn -c src/gunicorn/conf.py run

fi