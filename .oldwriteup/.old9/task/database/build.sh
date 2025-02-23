#!/bin/bash

docker rm -f database
docker rmi -f database

docker build -t database .
