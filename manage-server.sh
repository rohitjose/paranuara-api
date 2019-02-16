#!/bin/bash

if [ "$1" = "loadnrun" ]
then
    docker volume create --name=mongodb_data_volume
    docker-compose up -d
    sleep 3
    mongoimport --host localhost --port 27018 \
                --username mongouser --password supersecretpassword \
                --authenticationDatabase admin \
                --db paranuara --collection people --file resources/people.json --jsonArray
    mongoimport --host localhost --port 27018 \
                --username mongouser --password supersecretpassword \
                --authenticationDatabase admin \
                --db paranuara --collection companies --file resources/companies.json --jsonArray
    mongoimport --host localhost --port 27018 \
                --username mongouser --password supersecretpassword \
                --authenticationDatabase admin \
                --db paranuara --collection food --file resources/food.json --jsonArray
    echo "--- API Server ready to accept connections ---"
elif [ "$1" = "test" ]
then
    docker-compose run --rm app sh -c 'python manage.py test && flake8'
elif [ "$1" = "startapp" ]
then
    docker-compose run --rm app sh -c "python manage.py startapp $2"
elif [ "$1" = "run" ]
then
    docker-compose up -d
fi