#!/bin/sh

# install java
echo "*** Installing JAVA"
sudo add-apt-repository ppa:webupd8team/java && sudo apt-get update
sudo apt-get install oracle-jdk7-installer
echo "*** JAVA installed!"

echo "*** Installing dependencies"
sudo apt-get install -y sudo s3cmd python python-dev python-virtualenv libffi-dev vim iotop htop libev4 libev-dev
echo "*** Dependencies installed!"

echo "*** Checking python virtual env"
if [ ! -d /home/ubuntu/pyve1 ]
then
    echo "*** Creating new python virtual env"
    virtualenv /home/ubuntu/pyve1
    source /home/ubuntu/pyve1/bin/activate
    ./install.sh
fi

# install elasticsearch
echo "*** Installing Elasticsearch"
sudo wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.1.0/elasticsearch-2.1.0.deb
sudo dpkg -i elasticsearch-2.1.0.deb
sudo service elasticsearch start
echo "*** Elasticsearch installed!"

#cd /usr/share/elasticsearch/
# install marvel
#sudo bin/plugin install license
#sudo bin/plugin install marvel-agent
# start ES
#sudo service elasticsearch start
# install kibana
#sudo wget https://download.elastic.co/kibana/kibana/kibana-4.3.0-linux-x64.tar.gz
#sudo tar -xvf kibana-4.3.0-linux-x64.tar.gz
#cd kibana-4.3.0-linux-x64
# install the Marvel app into Kibana
#sudo bin/kibana plugin --install elasticsearch/marvel/latest
# start kibana
#sudo nohup ./kibana-4.3.0-linux-x64/bin/kibana &
