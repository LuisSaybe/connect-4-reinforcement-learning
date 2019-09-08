import tensorflow as tf
import time
from falcon.media.validators import jsonschema

from src.environment.connect_4.environment import Environment
from src.policy.q_epsilon_greedy import QEpsilonGreedyPolicy
from src.environment.connect_4.episode_generator import EpisodeGenerator

class TrainResource(object):
    def __init__(self, model):
        self.model = model

    def main(self, episode_count):
        agent_policy = QEpsilonGreedyPolicy(self.model, 0.1)
        generator = EpisodeGenerator(agent_policy, agent_policy, True)

        print('collecting', episode_count, 'episodes')

        start = time.time()
        episodes = generator.getMany(episode_count)

        x = []
        y = []

        for episode in episodes:
            final_reward = episode[-1][2]

            for sar in episode[:-1]:
              state = sar[0]
              action = sar[1]
              state_tensor = tf.one_hot([state], dtype='float32', depth=3)
              values = self.model.predict(state_tensor).tolist()[0]
              values[action] = final_reward

              x.append(state)
              y.append(values)

        print('fitting', len(x), 'points from ', episode_count, 'episodes')

        self.model.fit(
          tf.one_hot(x, dtype='float32', depth=3),
          tf.constant(y, shape=(len(y), Environment.COLUMNS))
        )

        end = time.time()

        print('duration', end - start)

    @jsonschema.validate({
        "type" : "integer",
        "minimum": 1
    })
    def on_post(self, req, resp):
        resp.media = 'ok'
        self.main(req.media)
