#!/bin/bash

docker-compose stop backend
docker container ls -a | grep backend | awk '{ print $1 }' | xargs podman container rm -f
docker-compose run --service-ports backend python manage.py runserver 0.0.0.0:8000
