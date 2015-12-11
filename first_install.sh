#!/bin/sh

# install elasticsearch
sudo wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.1.0/elasticsearch-2.1.0.deb
sudo dpkg -i elasticsearch-2.1.0.deb

cd /usr/share/elasticsearch/
# install marvel
sudo bin/plugin install license
sudo bin/plugin install marvel-agent
# start ES
sudo service elasticsearch start
# install kibana
sudo wget https://download.elastic.co/kibana/kibana/kibana-4.3.0-linux-x64.tar.gz
sudo tar -xvf kibana-4.3.0-linux-x64.tar.gz
cd kibana-4.3.0-linux-x64
# install the Marvel app into Kibana
sudo bin/kibana plugin --install elasticsearch/marvel/latest
# start kibana
sudo nohup ./kibana-4.3.0-linux-x64/bin/kibana &
