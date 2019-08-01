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
yaml_file = '../media/apispecs/index.yml'
model_file = ''

def publish_model(file_name, port, ip):

    print(file_name)
    if os.path.isfile(file_name):

        print('-'*50)
        print('Model exist on path')

        model_file = file_name

        thread = Thread(target = threaded_publish_model, args =(model_file, ip, port))
        thread.start()

    else:
        print('-'*50)
        print('There isnt model on path')
        print('-'*50)
        return



def threaded_publish_model(model_file, ip, port):
    print('thread is starting with file : {} and ip : {} port : {}'.format(model_file, ip, str(port)))
    app.run(host=ip, port=port)


@app.route('/', methods=['POST'])
@swag_from(yaml_file)
def test_model():

    h2o.init()
    model = h2o.load_model(model_file)

    math_score = request.args.get("math_score")
    reading_score = request.args.get("reading_score")
    writing_score = request.args.get("writing_score")
    cat_race_ethnicity = request.args.get("cat_race_ethnicity")
    cat_parental_level_of_education = request.args.get("cat_parental_level_of_education")
    cat_lunch = request.args.get("cat_lunch")
    cat_test_preparation_course = request.args.get("cat_test_preparation_course")


    prediction = model.predict(np.array([[math_score, reading_score, writing_score, cat_race_ethnicity, cat_parental_level_of_education,cat_lunch,cat_test_preparation_course]]))
    return str(prediction)
