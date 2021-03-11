#!/bin/bash
#chmod -R 755 ./bazaar
service mysql start 
service apache2 start
echo "Staring Java App"
java -Djava.net.useSystemProxies=true -server -jar dataturks-1.0-SNAPSHOT.jar server onprem.yml &
sleep 7
#Run node app
cd bazaar
echo "Staring npm run start-onprem"
npm run start-onprem &


# download the src directory
cd ..
pip3.8 install gdown
gdown https://docs.google.com/uc\?export\=download\&id\=1lxB93Nk1TYeyeqkS9-nLRHm01cRN-4HM -O dataturks_annotation_src.zip
unzip dataturks_annotation_src.zip

echo "start the python script"
cd ./dataturks_annotation_src
bash setup.sh $1 $2


while true; do sleep 1; done

