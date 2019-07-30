import h2o
from h2o.automl import H2OAutoML
from flask import Blueprint, Flask, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from
import numpy as np
import pandas as pd
import os.path
import subprocess
from threading import Thread
from time import sleep

from .models import ModelData

app = Flask(__name__)
swagger = Swagger(app)

model = None

def publish_model(file_name, port, ip):

    print(file_name)
    if os.path.isfile(file_name):

        print('-'*50)
        print('Model exist on path')
        h2o.init()
        model = h2o.load_model(file_name)

    else:
        print('-'*50)
        print('There isnt model on path')
        print('-'*50)
        return

    thread = Thread(target = threaded_publish_model, args =(file_name, ip, port))
    thread.start()

def threaded_publish_model(file_name, ip, port):
    app.run(host=ip, port=port)


@app.route('/')
@swag_from('../media/apispecs/index.yml')
def test_model():
    """Example endpoint for auto published model
    ---
    parameters:
      - name: s_length
        in: query
        type: number
        required: true
      - name: s_width
        in: query
        type: number
        required: true
      - name: p_length
        in: query
        type: number
        required: true
      - name: p_width
        in: query
        type: number
        required: true
      - name: a
        in: h
        type: string
        required: false
    """

    a = request.args.get("a")
    s_length = request.args.get("s_length")
    s_width = request.args.get("s_width")
    p_length = request.args.get("p_length")
    p_width = request.args.get("p_width")

    prediction = model.predict(np.array([[s_length, s_width, p_length, p_width]]))
    return str(prediction)
