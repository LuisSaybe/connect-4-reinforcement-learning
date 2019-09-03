from environment.connect_4.episode_generator import EpisodeGenerator
from policy.q_epsilon_greedy import QEpsilonGreedyPolicy

import tensorflow as tf

agent_q_model = tf.keras.Sequential([
  tf.keras.layers.Dense(7, input_shape=[6 * 7]),
])

agent_q_model.compile(
  optimizer='adam',
  loss='mean_squared_error',
  metrics=['accuracy']
)

agent_policy = QEpsilonGreedyPolicy(agent_q_model, 0.1)

generator = EpisodeGenerator(agent_policy, agent_policy, True)
episodes = generator.getMany(10)
