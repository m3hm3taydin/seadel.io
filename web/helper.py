import pandas as pd
import numpy as np
from web.pickle_helper import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from django.http import HttpResponse
import io
from io import BytesIO
import random
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def get_null_count(df):
    return df[df.isnull().any(axis=1)].shape[0]

def get_zero_count(df):
    return (df == 0).sum().sum()

def get_row_count(df):
    return df.shape[0]

def get_column_count(df):
    return df.shape[1]

def get_duplicated_count(df):
    return df.duplicated().sum()

def get_dtype_count(df):
    temp_df = df.dtypes.to_frame()
    temp_df.index.names = ['Column Name']
    temp_df.columns = ['Type']
    return temp_df.to_html()

def get_dtypes_as_dict(df):
    return df.dtypes.apply(lambda x: x.name).to_dict()



def get_null_rows_as_html(pk):
    df = get_or_save_dataframe(pk)
    return df[pd.isnull(df).any(axis=1)].to_html()

def get_zero_rows_as_html(pk):
    df = get_or_save_dataframe(pk)
    return df.loc[~(df==0).all(axis=1)].to_html()


def get_column_as_html(pk, column_name):
    df = get_or_save_dataframe(pk)
    return df[[column_name]].to_html()

def get_df_column_as_html(pk, count=200):
    df = get_or_save_dataframe(pk)
    return df.head(count).to_html()

def get_df_as_html(df, count=200):
    return df.head(count).to_html(classes='preview-table table table-striped table-bordered display compact nowrap')

def change_column_name(df, old_column, new_column):
    df.rename(columns={old_column: new_column}, inplace=True)
    #lets update pickle
    update_dataframe(df)
    return df

def drop_column(df, column_name):
    df.drop(column_name, axis=1, inplace=True)
    #lets update pickle
    update_dataframe(df)
    return df

def get_dummy_value_list(df, column_name):
    return df[column_name].value_counts().to_frame().to_html(classes="table")

def get_categorical_value_list(df, column_name):
    dummy, mapping_index = pd.Series(df[column_name]).factorize()
    dummy_df = pd.DataFrame({'col':mapping_index})
    return dummy_df.to_html(classes="table")

def create_dummy_columns (df, column_name):
    for column, count in df[column_name].value_counts().iteritems():
        df[column_name+'_'+column.replace(' ', '_')] = np.where(df[column_name].str.contains(column), 1, 0)

    #lets update pickle
    update_dataframe(df)
    return df

def create_categorical_column (df, column_name):
    df['cat_'+column_name], mapping_index = pd.Series(df[column_name]).factorize()
    #lets update pickle
    update_dataframe(df)
    return df

def remove_outlier(df, col_name):
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    new_df = df.loc[(df[col_name] > fence_low) & (df[col_name] < fence_high)]

    #lets update pickle
    update_dataframe(new_df)
    return new_df


def drop_null_rows(df):
    df.dropna(inplace = True)
    update_dataframe(df)

    return df

def get_outlier_rows(df, col_name):
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    return df.loc[(df[col_name] < fence_low) | (df[col_name] > fence_high)].to_html()

def get_outlier_image(df, col_name):

    fig, ax = plt.subplots()
    fig.add_subplot(111)

    df[[col_name]].boxplot(notch=True, widths=0.35, patch_artist=True, boxprops=dict(facecolor="C0"))

    ax.set_title('Column : {}'.format(col_name))
    ax.legend([col_name], loc='upper right')
    ax.set_xlim(0,6)

    # ax.set_xlabel("x label")
    # ax.set_ylabel("y label")


    canvas=FigureCanvas(fig)
    outstr = BytesIO()
    canvas.print_png(outstr)
    ret = base64.b64encode(outstr.getvalue())
    outstr.close()

    return ret.decode()


def save_dataframe(df):
    print('saved dataframe to {}'.format('saved_dataset.csv'))
    df.to_csv('saved_dataset.csv', sep=',')
