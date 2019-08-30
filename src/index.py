import tensorflow as tf
import tensorflow_probability as tfp
import math

def game(action):
    if action < -4 or action > 2:
        return -1
    return math.sin(action)

def make_distribution_fn(t):
    return tfp.distributions.Normal(loc=t, scale=t, validate_args=True)

def convert_to_tensor_fn(s):
    return s.sample(5)

action_model = tf.keras.Sequential([
  tf.keras.layers.Dense(2, input_dim=2),
  tfp.layers.DistributionLambda(
    make_distribution_fn=make_distribution_fn,
    convert_to_tensor_fn=convert_to_tensor_fn
  )
])

tensor = tf.constant([
  [1.0, 2.0]
], dtype='float32')

out = action_model.predict(tensor)

print(out)
