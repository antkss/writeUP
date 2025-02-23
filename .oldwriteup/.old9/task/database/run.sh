#!/bin/bash

docker rm -f database
docker run -d -p 18439:18439 --name database --restart unless-stopped --privileged database
