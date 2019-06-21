import pandas as pd
import numpy as np
from web.pickle_helper import *
import matplotlib
matplotlib.use('Agg') # watch this line
import matplotlib.pyplot as plt
import mpld3
import random
import seaborn as sns
import io
from io import BytesIO
import random
import base64

plt.ioff() # and this one


def get_image_test(df, col_name):

    fig, ax = plt.subplots()
    # ax.boxplot(df[[col_name]], 0, 'gD')

    df[[col_name]].boxplot(notch=True)

    # ax.set_title('Column : {}'.format(col_name))
    ax.legend([col_name], loc='upper right')

    plt.close() # and this one

    return mpld3.fig_to_html(fig)

def get_seaborn_image(df, col_name):
    plt.figure()
    img = BytesIO()
    sns.set_style("dark") #E.G.

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]

    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    ret = base64.b64encode(img.getvalue())
    img.close()

    return ret.decode()

def get_column_boxplot(df, col_name):
    plt.figure()
    img = BytesIO()
    sns.boxplot( y=df[col_name], width=0.5, palette="Blues" )

    plt.savefig(img, format='png')
    img.seek(0)

    ret = base64.b64encode(img.getvalue())
    img.close()

    return ret.decode()

# def generate_bar_chart(df, x, y, z=None, chart_title="Chart Title", chart_size_x=12, chart_size_y=12):
def generate_chart_image(df, x, y, **kwargs):

    # for key, value in kwargs.items():
    #     print(key + " ===== " + value)
    #
    # print("x ===== " + x)
    # print("y ===== " + y)
    plt.figure()


    if 'chart_size_x' in kwargs and 'chart_size_y' in kwargs:
        plt.figure(figsize=(int(kwargs['chart_size_x']),int(kwargs['chart_size_y'])))
    img = BytesIO()

    if 'chart-type' in kwargs:
        if kwargs['chart-type'] == 'bar':
            sns.barplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'line':
            sns.lineplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'scatter':
            sns.scatterplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'box':
            sns.boxplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'violin':
            sns.violinplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'joint':
            #got error
            sns.jointplot( y=y, x=x, data=df, kind="hex").set_title(kwargs['chart_title'])
        elif kwargs['chart-type'] == 'dist':
            #got error
            f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
            sns.distplot(y, color="m", ax=axes[1, 1])
            # sns.distplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])

    else:
        sns.barplot( y=y, x=x, hue=kwargs['z'], data=df,palette="Blues" ).set_title(kwargs['chart_title'])

    plt.savefig(img, format='png')
    img.seek(0)

    ret = base64.b64encode(img.getvalue())
    img.close()

    return ret.decode()


def generate_column_image(df, x, y, **kwargs):

    plt.figure()


    if 'chart_size_x' in kwargs and 'chart_size_y' in kwargs:
        plt.figure(figsize=(int(kwargs['chart_size_x']),int(kwargs['chart_size_y'])))
    img = BytesIO()


    sns.barplot(x=df[y].value_counts().index, y=df[y].value_counts(), palette="Blues" ).set_title(kwargs['chart_title'])

    plt.savefig(img, format='png')
    img.seek(0)

    ret = base64.b64encode(img.getvalue())
    img.close()

    return ret.decode()
