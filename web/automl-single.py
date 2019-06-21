import pandas as pd
import numpy as np

import h2o
from h2o.automl import H2OAutoML

import os

#this file can run alone
#then we can get stdout with subprocess

def run_auto_analyse_single(train, test, target, max_models = 2):

    h2o.init()

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
    aml = H2OAutoML(max_models= max_models, seed=1)
    aml.train(x=x, y=y, training_frame=train)

    # View the AutoML Leaderboard
    lb = aml.leaderboard

    print('*'*50)
    print(os.getcwd())
    # for now save the model
    model_path = h2o.save_model(model=aml.leader, path="media/models/mymodel", force=True)
    # and save the test schema for auto flask input
    testdf.head(1).to_csv('media/modelschemas/testschema.csv')

    #lb.head(rows=lb.nrows)  # Print all rows instead of default (10 rows)
    df = lb.as_data_frame()
    return df
