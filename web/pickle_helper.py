import numpy as np
import pandas as pd
import os
from .models import Document
from django.contrib.sites.shortcuts import get_current_site

pickle_path = "media/pickles"

def get_or_save_dataframe(pk):
    document = Document.objects.get(pk=pk)
    print('document primary key is : {}'.format(str(pk)))
    try:
        if document.updated == 1:
            print('document setting is updated or this is a new document lets try to reload pickle')
            return reload_pickle(document)
        print('lets load the pickle')
        df = pd.read_pickle(os.path.join(pickle_path, 'cached_dataframe__' + str(document.pk) + '__.pkl'))
        print('pickle loaded to df')
        return df
    except:
        return reload_pickle(document)


def reload_pickle(document):
    document_url = document.document_url
    print('document_url : {}'.format(document_url))
    if document.file.name.endswith('.csv'):
        print('document file name : {}'.format(document.file.name))
        print('document file name endswith csv')
        if document.row_count == 0:
            df = pd.read_csv(document_url, sep=document.seperator, encoding=document.encoding)
        else:
            df = pd.read_csv(document_url, sep=document.seperator, nrows=document.row_count, encoding=document.encoding)
        document.updated=0
        document.save()
        print('document saved')
    elif document.file.name.endswith('.xlsx'):
        print('document file name : {}'.format(document.file.name))
        print('document file name endswith xlsx')
        #for now only get first sheet of excel
        xl = pd.ExcelFile(document_url)
        df = xl.parse(xl.sheet_names[0])
        document.updated=0
        document.save()
        print('document saved')
    else:
        print('Error : Not implemented file extension')
        return
    df = fix_column_names(df)
    print('Fixed Dataframe column names')
    print('trying to save pickle file')
    print('test')
    print('*' * 50)
    print(os.getcwd())
    # pickle path exists ?
    if(os.path.exists(pickle_path) is False):
        print('creating the pickle folder')
        os.mkdir(pickle_path)
    else:
        print('pickle folder exist')
        try:
            df.to_pickle(os.path.join(pickle_path, 'cached_dataframe__' + str(document.pk) + '__.pkl'))
            print('saved pickle file')

        except:
            print('Error : Can not save pickle to pickles/cached_dataframe__' + str(document.pk) + '__.pkl')


    return df

def update_dataframe(df):
    document = Document.objects.get(is_active=True)
    df = fix_column_names(df)
    df.to_pickle(os.path.join(pickle_path, 'cached_dataframe__' + str(document.pk) + '__.pkl'))

def fix_column_names(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace(':', '')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace("'", '')
    return df
