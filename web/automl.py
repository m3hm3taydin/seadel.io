import pandas as pd
import numpy as np

import subprocess
import re
from psutil import process_iter
from signal import SIGTERM

import h2o
from h2o.automl import H2OAutoML

import os
import random
import socket

from .models import ModelData
from .publish_model import publish_model


def run_auto_analyse(train, test, target, max_models=2):
    h2o.init(strict_version_check = False)

    testdf = test
    train = h2o.H2OFrame(train)
    test = h2o.H2OFrame(test)

    # Identify predictors and response
    x = train.columns
    y = target
    x.remove(y)

    # For binary classification, response should be a factor
    train[y] = train[y].asfactor()
    test[y] = test[y].asfactor()

    # Run AutoML for 20 base models (limited to 1 hour max runtime by default)
    aml = H2OAutoML(max_models=max_models, seed=1)
    aml.train(x=x, y=y, training_frame=train)

    # View the AutoML Leaderboard
    lb = aml.leaderboard

    print('*' * 50)
    print(os.getcwd())
    
    model_path = "media/models"
    model_schemas_path = "media/modelschemas"
    # model and schemas directories exists ?
    if(os.path.exists(model_path) is False):
       os.mkdir(model_path)

    if(os.path.exists(model_schemas_path) is False):
       os.mkdir(model_schemas_path)
    # for now save the model
    model_path = h2o.save_model(
        model=aml.leader, path=model_path + "/mymodel", force=True)
    # and save the test schema for auto flask input
    testdf.drop(target, axis=1, inplace=True)

    sample_path = model_schemas_path + '/testschema_' + \
        str(random.randint(10000, 99999)) + '.csv'
    testdf.head(1).to_csv(sample_path)

    newlb = lb.as_data_frame()
    selected_model = newlb['model_id'][0]
   
    auc = ''
    logloss = ''
    mean_per_class_error = ''
    rmse = ''
    mse = ''
    if 'auc' in newlb:
        auc = newlb['auc'][0]

    if 'logloss' in newlb:
        logloss = newlb['logloss'][0]

    if 'mean_per_class_error' in newlb:
        mean_per_class_error = newlb['mean_per_class_error'][0]

    if 'rmse' in newlb:
        rmse = newlb['rmse'][0]
   
    if 'mse' in newlb:
        mse = newlb['mse'][0]

    port = find_free_port()
    ip = '0.0.0.0'
    print('*' * 50)
    print(str(port))
    status = True

    new_model = ModelData(sample_path=sample_path, model_path=model_path, selected_models=selected_model, auc=auc,
                          logloss=logloss, mean_per_class_error=mean_per_class_error, rmse=rmse, mse=mse, port=port, ip=ip, status=status)
    new_model.save()

    # lb.head(rows=lb.nrows)  # Print all rows instead of default (10 rows)
    df = lb.as_data_frame()

    publish_model(model_path, port, ip)
    print('*' * 50)
    print('Model Published on:')
    print('port : {}'.format(port))
    print('ip : {}'.format(ip))
    print('model file : {}'.format(model_path))
    print('*' * 50)
    return df


def find_free_port():
    s = socket.socket()
    s.bind(('', 0))            # Bind to a free port provided by the host.
    return s.getsockname()[1]

def get_pids(port):

	command = "lsof -i :%s | awk '{print $2}'" % port
	pids = subprocess.check_output(command, shell=True)
	return pids.strip().decode('UTF-8').splitlines()


def kill_pids(port):

    # port = args[0]
    pid = get_pids(port)
    if(len(pid) == 2):
        print('pid is : {}'.format(pid[1]))
        print('lets try to kill...')
        command = 'kill -9 {}'.format(pid[1])
        # os.system(command)

        #problem : we started flask with thread so we need to kill thread not pids
        #fix later
        print('done.')


def start_model(file_name, port, ip):
    publish_model(file_name, port, ip)
