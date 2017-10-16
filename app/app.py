from flask import Flask, request, g, jsonify, make_response, render_template
import os
import random
import subprocess
from flask_sqlalchemy import SQLAlchemy
import time

from grpc.beta import implementations
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

from models import db
db.init_app(app)
from models import TrainedModel


@app.before_request
def before_request():
    g.request_start_time = time.gmtime()
    g.request_time = lambda: "%.5fs" % (time.gmtime() - g.request_start_time)


@app.route('/')
def index():
    return render_template('list.html')


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
    # TODO: if model is missing, this line causes bad_request response
    # modelFile = request.files['model']
    trainedModel = TrainedModel(name)
    db.session.add(trainedModel)
    db.session.commit()
    return jsonify(trainedModel.serialize)


@app.route('/models/<string:id>', methods=['PUT', 'PATCH'])
def updateModel(id):
    name = request.form['name']
    # TODO: if model is missing, this line causes bad_request response
    # modelFile = request.files['model']
    found = TrainedModel.query.filter_by(hash_id = id).first()
    if found:
        if name:
            found.name = name
        # TODO: handle model file update
        db.session.commit()
        return jsonify(found.serialize)
    else:
        return make_response('not found', 404)


@app.route('/models/<string:id>', methods=['DELETE'])
def deleteModel(id):
    found = TrainedModel.query.filter_by(hash_id = id).first()
    if found:
        db.session.delete(found)
        db.session.commit()
        return "deleted {}\n".format(found.hash_id)
    else:
        return make_response('not found', 404)



@app.route('/predictions', methods=['POST'])
def createPrediction():
    model = request.form['model']
    imageFile = request.files['image']
    predicted = _predict(imageFile, model)
    return str(predicted)


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
