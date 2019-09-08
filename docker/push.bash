#!/bin/bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t luissaybe/tf-connect4 .
docker push luissaybe/tf-connect4:latest
docker logout
