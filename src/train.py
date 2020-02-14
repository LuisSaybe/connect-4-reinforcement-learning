import itertools
import os
import sys
import time
import multiprocessing

import tensorflow as tf

from environment.connect_4.environment import Environment
from environment.connect_4.episode_generator import EpisodeGenerator
from resource.prediction import PredictionResource
from policy.q_epsilon_greedy import QEpsilonGreedyPolicy
from resource.cors import CORS

MODEL_PATH = '/tmp/model/model.h5'

model = tf.keras.Sequential([
  tf.keras.layers.Flatten(input_shape=[Environment.ROWS * Environment.COLUMNS, 3]),
  tf.keras.layers.Dense(7, input_shape=[Environment.ROWS * Environment.COLUMNS * 3]),
])

model.compile(
  optimizer=tf.keras.optimizers.SGD(lr=0.01),
  loss='mean_squared_error',
  metrics=['accuracy']
)

def collect(episode_count):
    agent_policy = QEpsilonGreedyPolicy(model, 0.1)
    generator = EpisodeGenerator(agent_policy, agent_policy)
    episodes = generator.getMany(episode_count)

    x = []
    y = []

    for episode in episodes:
        final_reward = episode[-1][2]
        states = list(map(lambda sar : sar[0], episode))
        predictions = model.predict(tf.one_hot(states, dtype='float32', depth=3)).tolist()

        for index in range(len(episode) - 1):
          state = episode[index][0]
          action = episode[index][1]
          values = predictions[index]
          values[action] = final_reward

          x.append(state)
          y.append(values)

    return x, y

iterations = int(sys.argv[1])
epsides_count = int(sys.argv[2])

for i in range(iterations):
    print('iteration', i + 1, 'of', iterations)

    start = time.time()

    print('collecting', epsides_count, 'episodes')

    x, y = collect(epsides_count)

    print('fitting', len(x), 'points')

    model.fit(
      tf.one_hot(x, dtype='float32', depth=3),
      tf.constant(y, shape=(len(y), Environment.COLUMNS))
    )

    model.save(MODEL_PATH)

    end = time.time()
    print('duration:', end - start)
