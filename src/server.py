import tensorflow as tf
import falcon
from wsgiref import simple_server

from environment.connect_4.environment import Environment
from resource.prediction import PredictionResource
from resource.cors import CORS

MODEL_PATH = '/tmp/model/model.h5'
api = falcon.API(middleware=[CORS()])
api.add_route('/predict', PredictionResource(MODEL_PATH))

if __name__ == '__main__':
    httpd = simple_server.make_server('', 8000, api)
    print('listening on 8000')
    httpd.serve_forever()
