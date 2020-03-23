#!/bin/bash

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t luissaybe/connect-4-reinforcement-learning .
docker push luissaybe/connect-4-reinforcement-learning:latest
docker logout
