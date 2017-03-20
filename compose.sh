#!/bin/bash

sudo apt-get install python-pip
sudo pip install docker-compose
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up
