# DataTurks
ML data annotations made super easy for teams. Just upload data, add your team and build training/evaluation dataset in hours.

#### First install maven if haven't already. On macOS, run:
```
brew install maven
```

#### To build a docker image, run:
```
cd hope
mvn package -DskipTests
cd ..
docker build -t MY_TAG . -f ./hope/docker/Dockerfile
```

#### To start a docker container that hosts the UI of Dataturks, run:
```
docker run -d -p 80:80 my_dataturks_image
```

#### To get access to the Dataturks UI, go to http://localhost/projects/login from your preferred browser.
