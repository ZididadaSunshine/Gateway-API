#!/bin/bash

docker stop gateway
docker rm gateway
docker rmi gateway
docker build -t gateway .
docker run --name gateway -p 5000:5000 -d gateway
