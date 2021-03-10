#!/bin/bash

# pull the dataturks image if needed
if [[ -n "$( docker images -q stlin0717/dataturks )" ]]
then
    echo "image alreadly downloaded!"
else
    echo "Pull the dataturks image from https://hub.docker.com/repository/docker/stlin0717/dataturks..."
    docker pull stlin0717/dataturks
fi

# run the docker container
docker run -d -p 80:80 --name dataturks stlin0717/dataturks

echo "Waiting for the container to start..."
sleep 10

# build python virtual environment
if [ ! -d "./.env" ]
then
    echo "setup virtual enviroment..."
    python3 -m venv ./.env
    source ./.env/bin/activate
    .env/bin/python -m pip install --upgrade pip
    pip3 install requests
else
    echo "virtual enviroment setup already!"
    python3 -m venv ./.env
    source ./.env/bin/activate
fi

# create projects
echo ""
python3 dataturks_api.py --email $1 --workflow $2
