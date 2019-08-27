#!/bin/bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t luissaybe/tf-gridworld .
docker push luissaybe/tf-gridworld:latest
docker logout
