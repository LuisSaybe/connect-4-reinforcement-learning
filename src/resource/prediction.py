import os.path
import tensorflow as tf
import falcon
from falcon.media.validators import jsonschema

from environment.connect_4.environment import Environment

class PredictionResource(object):
    def __init__(self, model_path):
        self.model_path = model_path

    @jsonschema.validate({
        "type" : "array",
        "maxItems": Environment.ROWS * Environment.COLUMNS,
        "minItems": Environment.ROWS * Environment.COLUMNS,
        "items": [
            { "enum": [ Environment.EMPTY, Environment.AGENT, Environment.ADVERSARY ] }
        ]
    })
    def on_post(self, req, resp):
        if os.path.isfile(self.model_path):
            state = req.media
            state_tensor = tf.one_hot([state], dtype='float32', depth=3)
            model = tf.keras.models.load_model(self.model_path)
            state_action_values = model.predict(state_tensor).tolist()[0]
            resp.media = state_action_values
        else:
            resp.media = [ 0 ] * Environment.COLUMNS
