#!/bin/bash
echo "Updating dependencies..."
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python-cherrypy3
sudo apt-get install mongodb python-pip build-essential python-dev python-setuptools python-zmq python-sklearn -y
sudo pip install -r requirements.txt
