import time
import tensorflow as tf
import falcon
from falcon.media.validators import jsonschema

from environment.connect_4.environment import Environment
from environment.connect_4.episode_generator import EpisodeGenerator
from policy.q_epsilon_greedy import QEpsilonGreedyPolicy

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

start = time.time()

episodes = generator.getMany(10)

end = time.time()

print('duration', end - start)

class Resource(object):
    schema = {
        "type" : "array",
        "maxItems": 6 * 7,
        "minItems": 6 * 7,
        "items": [
            { "enum": [ Environment.EMPTY, Environment.AGENT, Environment.ADVERSARY ] },
            { "type": "string" }
        ]
    }

    @jsonschema.validate(Resource.schema)
    def on_post(self, req, resp):
        message = req.media.get('message')
        resp.media = {'message': message}
