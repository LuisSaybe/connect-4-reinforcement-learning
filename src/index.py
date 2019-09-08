from multiprocessing import Process
import tensorflow as tf
import falcon

from src.environment.connect_4.environment import Environment
from src.resource.prediction import PredictionResource
from src.resource.train import TrainResource
from src.resource.cors import CORS

agent_q_model = tf.keras.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(7, input_shape=[Environment.ROWS * Environment.COLUMNS * 3], activation='linear'),
])

agent_q_model.compile(
  optimizer=tf.keras.optimizers.SGD(lr=0.01),
  loss='mean_squared_error',
  metrics=['accuracy']
)

api = falcon.API(middleware=[CORS()])
api.add_route('/predict', PredictionResource(agent_q_model))
api.add_route('/train', TrainResource(agent_q_model))
