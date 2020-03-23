## connect 4 with tensorflow 2

Reinforcement Learning, Sutton, Barto
Chapter 9: On-policy Prediction with Approximation

#### build

start training

```sh
docker-compose up
```

play a game

```sh
docker run \
  -it \
  --name connect-4-play \
  --rm \
  -v $(pwd):/tmp/project \
  connect-4-reinforcement-learning_trainer python3 /tmp/project/src/play.py
```
