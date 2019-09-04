import ray
import time

from environment.connect_4.episode_generator import EpisodeGenerator
from policy.q_epsilon_greedy import QEpsilonGreedyPolicy

ray.init()

@ray.remote
def getMany(n):
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
    return generator.getMany(n)

'''
read this doc for tf parallel execution
https://ray.readthedocs.io/en/latest/using-ray-with-tensorflow.html

stats
[ 5 ] * 1   takes 7 seconds
[ 5 ] * 5   takes 20 seconds
[ 5 ] * 10  takes 33 seconds
[ 5 ] * 100 takes ?
'''

start = time.time()

futures = [ getMany.remote(n) for n in [ 5 ] * 100 ]
results = ray.get(futures)

end = time.time()

print('duration', end - start)
