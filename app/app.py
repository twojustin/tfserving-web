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
    model = request.form['model']
    imageFile = request.files['image']
    predicted = _predict(imageFile, model)
    return "create prediction model={}, image={}, predict={}\n".format(model, imageFile, predicted)


def _randomHash():
    return random.getrandbits(32)


def _predict(input, model):
    channel = implementations.insecure_channel('tensorflow-serving', 9000)
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model
    request.model_spec.signature_name = 'predict_images'
    request.inputs['images'].CopyFrom(
        tf.contrib.util.make_tensor_proto(input.read(), shape=[1]))
    return stub.Predict(request, 10.0)  # 10 secs timeout

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
