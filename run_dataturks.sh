#!/bin/bash

# pull the dataturks image if needed
if [[ -n "$( docker images -q stlin0717/dataturks:wscript )" ]]
then
    echo "image alreadly downloaded!"
else
    echo "Pull the dataturks image from https://hub.docker.com/repository/docker/stlin0717/dataturks..."
    docker pull stlin0717/dataturks:wscript
fi

# run the docker container
docker run -d -p 80:80 --name dataturks stlin0717/dataturks:wscript "$1" "$2"
