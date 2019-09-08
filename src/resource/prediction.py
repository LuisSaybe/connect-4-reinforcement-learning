import tensorflow as tf
import falcon
from falcon.media.validators import jsonschema

from src.environment.connect_4.environment import Environment

class PredictionResource(object):
    def __init__(self, model):
        self.model = model

    @jsonschema.validate({
        "type" : "array",
        "maxItems": Environment.ROWS * Environment.COLUMNS,
        "minItems": Environment.ROWS * Environment.COLUMNS,
        "items": [
            { "enum": [ Environment.EMPTY, Environment.AGENT, Environment.ADVERSARY ] }
        ]
    })
    def on_post(self, req, resp):
        state = req.media
        state_tensor = tf.one_hot([state], dtype='float32', depth=3)
        state_action_values = self.model.predict(state_tensor).tolist()[0]
        resp.media = state_action_values
