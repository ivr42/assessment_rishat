#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"


if [[ ! -e /${CONTAINER_FIRST_STARTUP} ]]; then

    touch /${CONTAINER_FIRST_STARTUP}

    # Apply database migrations
    echo "Apply database migrations"
    python manage.py migrate

    # Collect static files
    echo "Collect static files"
    python manage.py collectstatic --noinput

fi


echo "Starting the gunicorn server"
gunicorn test_shop.wsgi:application --bind 0:8000

