import numpy as np
import pandas as pd
from .models import Document
from django.contrib.sites.shortcuts import get_current_site


def get_or_save_dataframe(pk):
    document = Document.objects.get(pk=pk)
    try:
        if document.updated == 1:
            return reload_pickle(document)
        df = pd.read_pickle('pickles/cached_dataframe__' + str(pk) + '__.pkl')
        return df
    except:
        return reload_pickle(document)


def reload_pickle(document):
    document_url = document.url
    if document.file.name.endswith('.csv'):
        if document.row_count == 0:
            df = pd.read_csv(document_url, sep=document.seperator, encoding=document.encoding)
        else:
            df = pd.read_csv(document_url, sep=document.seperator, nrows=document.row_count, encoding=document.encoding)
        document.updated=0
        document.save()
    elif document.file.name.endswith('.xlsx'):
        #for now only get first sheet of excel
        xl = pd.ExcelFile(document_url)
        df = xl.parse(xl.sheet_names[0])
        document.updated=0
        document.save()

    else:
        return
    df = fix_column_names(df)
    df.to_pickle('pickles/cached_dataframe__' + str(document.pk) + '__.pkl')
    return df

def update_dataframe(df):
    document = Document.objects.get(is_active=True)
    df = fix_column_names(df)
    df.to_pickle('pickles/cached_dataframe__' + str(document.pk) + '__.pkl')

def fix_column_names(df):
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace(':', '')
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace("'", '')
    return df
