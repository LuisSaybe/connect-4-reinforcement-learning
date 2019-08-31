import tensorflow as tf
import tensorflow_probability as tfp
import math

def game(action):
    if action < -4 or action > 2:
        return -1
    return math.sin(action)

action_model = tf.keras.Sequential([
  tf.keras.layers.Dense(1),
  tf.keras.layers.Lambda(lambda t : tf.keras.backend.clip(t, 1, 10)),
  tfp.layers.DistributionLambda(
    make_distribution_fn=lambda t : tfp.distributions.Normal(loc=t, scale=t)
  )
])

action_model.compile(
  optimizer='adam',
  loss='mean_squared_error',
  metrics=['accuracy']
)

value_model = tf.keras.Sequential([
  tf.keras.layers.Dense(1),
])

value_model.compile(
  optimizer='adam',
  loss='mean_squared_error',
  metrics=['accuracy']
)

for _ in range(10):
    state = tf.constant([ [0.0] ], dtype='float32')
    action = action_model.predict(state)
    reward = game(action)
    next_state = tf.constant([ [0.0] ], dtype='float32')
    delta = reward + value_model.predict(next_state) + value_model.predict(state)

    print('reward', reward)
