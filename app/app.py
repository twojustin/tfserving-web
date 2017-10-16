from flask import Flask, request, jsonify
import os
import random
import subprocess
from flask_sqlalchemy import SQLAlchemy

from grpc.beta import implementations
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

from models import db
db.init_app(app)
from models import TrainedModel


@app.route('/')
def index():
    command = 'pwd'
    result = subprocess.check_output([command], shell=True)
    return "Meow, {}.\n".format(result)


@app.route('/models')
def listModels():
    models = TrainedModel.query.all()
    a = []
    for m in models:
        a.append(m.serialize)
    return jsonify(a)


@app.route('/models', methods=['POST'])
def createModel():
    name = request.form['name']
    modelFile = request.files['model']
    trainedModel = TrainedModel(name)
    db.session.add(trainedModel)
    db.session.commit()
    return "create model name={}\n".format(name)


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
    return "{}\n".format(predicted)


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
