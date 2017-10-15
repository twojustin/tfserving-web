from redis import Redis
from flask import Flask, request
import os
import random
import subprocess

from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def index():
    count = redis.incr('hits')
    return "Meow, {}.\n".format(count)


@app.route('/models')
def listModels():
    command = 'pwd'
    result = subprocess.check_output([command], shell=True)
    return 'list models, pwd={}\n'.format(result)


@app.route('/models', methods=['POST'])
def createModel():
    params = request.get_json()
    desc = params['short_description']
    hashId = _randomHash()
    return "create model short_description={}, hash={}\n".format(desc, hashId)


@app.route('/models/<string:id>', methods=['PUT', 'PATCH'])
def updateModel(id):
    return "update model {}\n".format(id)


@app.route('/models/<string:id>', methods=['DELETE'])
def deleteModel(id):
    return "delete model {}\n".format(id)


@app.route('/predictions', methods=['POST'])
def createPrediction():
    modelName = request.form['model']
    imageFile = request.files['image']
    return "create prediction model={}, image={}\n".format(modelName, imageFile)


def _randomHash():
    return random.getrandbits(32)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
