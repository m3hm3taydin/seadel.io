from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (View,TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from web.forms import DocumentForm
import numpy as np
import pandas as pd
from web.helper import *
from web.automl import *
from .chart_helper import *
import urllib.parse
import time
from django.http import HttpResponse, Http404, JsonResponse
import pickle
import math
from mimetypes import guess_type
from .models import Document, ModelData


class IndexView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class DataSourceView(TemplateView):
    template_name = './ops/data_source.html'

class NullModal(TemplateView):
    template_name = './modals/get_null_rows.html'

def send_file(request):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    df = get_selected_dataframe(request)
    save_dataframe(df)
    filename = 'saved_dataset.csv'

    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type=guess_type(filename)[0])
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        print('size : {}'.format(len(response.content)))
        print('filename : {}'.format(filename))
        print('content type : {}'.format(guess_type(filename)[0]))
        print(response)
        return response

def modal_show(request, operation):
    print(operation)

    if operation == 'null':
        context = {'return_data': get_null_rows_as_html(get_current_document().pk),
        }
        return render(request, 'modals/get_null_rows.html', context)
    if operation == 'zero':
        context = {'return_data': get_zero_rows_as_html(get_current_document().pk),
        }
        return render(request, 'modals/get_null_rows.html', context)
    if '-' in operation:
        if 'changecolumn' in operation:
            column = operation.split('-')
            context = {'old_column': column[1],
            }
            return render(request, 'modals/change_column.html', context)
        if 'dropcolumn' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
            }
            return render(request, 'modals/drop_column.html', context)
        if 'createdummy' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
                        'value_list': get_dummy_value_list(get_selected_dataframe(request), column[1])
            }
            return render(request, 'modals/create_dummy_variable_modal.html', context)
        if 'createcategorical' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
                        'value_list': get_categorical_value_list(get_selected_dataframe(request), column[1])
            }
            return render(request, 'modals/create_cat_variable_modal.html', context)
        if 'removeoutlier' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
                        'value_list': get_outlier_rows(get_selected_dataframe(request), column[1])
            }
            return render(request, 'modals/remove_outliers_modal.html', context)
        if 'lookoutlier' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
                        'value_list' : get_column_boxplot(get_selected_dataframe(request), column[1])
            }
            return render(request, 'modals/look_outliers_modal.html', context)
        if 'wordcloud' in operation:
            column = operation.split('-')
            context = {'column_name': column[1],
                        'value_list' : get_wordcloud_image(get_selected_dataframe(request), column[1])
            }
            return render(request, 'modals/word_cloud.html', context)
        if 'all' in operation:
            document_pk = operation.split('-')
            context = {'return_data': get_df_column_as_html(document_pk[1]),}
            return render(request, 'modals/get_all_rows.html', context)
        if 'settings' in operation:
            document_pk = operation.split('-')
            document = Document.objects.get(pk=document_pk[1])

            context = {'document': document,}
            return render(request, 'modals/file_settings.html', context)


        column = operation.split('-')
        context = {'return_data': get_column_as_html(get_current_document().pk, column[1]),
        }
        return render(request, 'modals/get_null_rows.html', context)



def visualize_data(request):
    print('------ visualize_data view ------')
    #first get selected dataframe
    df = get_selected_dataframe(request)
    if type(df) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        #set default parameters
        parameters = {}
        parameters['chart_size_x'] = '7'
        parameters['chart_size_y'] = '7'
        parameters['chart_title'] = 'Chart Title'

        context = {'columns': get_dtypes_as_dict(df),
            'parameters' : parameters,
        }
        return render(request, 'ops/visualize_data.html', context)


def generate_chart(request):
    print('------ generate_chart view ------')
    #first get selected dataframe
    selected_dataframe = get_selected_dataframe(request)
    if type(selected_dataframe) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        df = selected_dataframe
        column_types = get_dtypes_as_dict(df)

        parameters = {}

        # set defaults
        parameters['z'] = None
        # x = []
        for key, value in request.POST.items():
            if value == 'on':
                parameters[key] = value
                if 'int' in column_types[key]:
                    y = key
                else:
                    if 'x' in vars():
                        parameters['z'] = key
                    else:
                        x = key
            else:
                parameters[key] = value


        if 'x' not in vars() or 'y' not in vars():
            context = {'columns': column_types,}
        else:

            context = {'columns': column_types,
                'generated_chart' : generate_chart_image(selected_dataframe, x, y, **parameters),
                'parameters' : parameters,
            }

        return render(request, 'ops/visualize_data.html', context)

def publish_model(request):

    model_list = ModelData.objects.all()
    return render(request, 'ops/publish_model.html', {'model_list': model_list})

def analyse_data(request):

    print('------ analyse_data view ------')
    selected_dataframe = get_selected_dataframe(request)
    if type(selected_dataframe) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        return render(request, 'ops/analyse_data.html')


def analyse_prediction(request):
    print('------ analyse_prediction view ------')

    selected_dataframe = get_selected_dataframe(request)
    if type(selected_dataframe) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        return render(request, 'ops/analyse_prediction.html')

def analyse_prediction_auto(request):
    df = get_selected_dataframe(request)
    if type(df) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        column_types = get_dtypes_as_dict(df)
        if request.method == 'POST':
            if 'selected_target' in request.POST:
                selected_target = request.POST['selected_target']

                print('selected target : {}'.format(selected_target))

                msk = np.random.rand(len(df)) < 0.8
                train = df[msk]
                test = df[~msk]
                result_df = run_auto_analyse(train, test, selected_target, 10)

                context = {'return_data': result_df.to_html(), 'columns': column_types,
                }
                return render(request, 'ops/analyse_prediction_auto.html', context)
            else:
                print('target not selected')

                context = {'return_data': '', 'columns': column_types,
                }
                return render(request, 'ops/analyse_prediction_auto.html', context)

        if request.method == 'GET':

            context = {'return_data': '', 'columns': column_types,
            }
            return render(request, 'ops/analyse_prediction_auto.html', context)




def analyse_clustering(request):
    print('------ analyse_clustering view ------')
    selected_dataframe = get_selected_dataframe(request)
    if type(selected_dataframe) == type(False):
        document_list = Document.objects.all()
        return render(request, 'ops/upload_file.html', {'documents': document_list})
    else:
        return render(request, 'ops/analyse_clustering.html')

def file_settings(request):
    print('------ file_settings view ------')
    if request.method == 'POST':
        if 'seperator' in request.POST:
            seperator = request.POST['seperator']
        if 'row_count' in request.POST:
            row_count = request.POST['row_count']
        if 'encoding' in request.POST:
            encoding = request.POST['encoding']
        if 'headerRow' in request.POST:
            headerRow = 0
        else:
            headerRow = 1
        if 'document_pk' in request.POST:
            document_pk = request.POST['document_pk']

        document = Document.objects.get(pk=document_pk)

        document.seperator = seperator
        document.row_count = row_count
        document.encoding = encoding
        document.headerRow = headerRow
        document.updated = 1
        document.save()

    document_list = Document.objects.all()
    return render(request, 'ops/upload_file.html', {'documents': document_list})


def data_prepare(request):
    if request.method == 'POST':
        if 'newColumnName' in request.POST:
            newColumnName = request.POST['newColumnName']
            oldColumnName = request.POST['oldColumnName']
            print('*'*50)
            print('new Column Name : {}'.format(newColumnName))
            print('old Column Name : {}'.format(oldColumnName))
            df = change_column_name(get_selected_dataframe(request), oldColumnName, newColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)

        if 'dropColumnName' in request.POST:
            dropColumnName = request.POST['dropColumnName']
            print('drop Column Name : {}'.format(dropColumnName))
            df = drop_column(get_selected_dataframe(request), dropColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)

        if 'dummyColumnName' in request.POST:
            dummyColumnName = request.POST['dummyColumnName']
            print('Dummy Column Name : {}'.format(dummyColumnName))
            df = create_dummy_columns(get_selected_dataframe(request), dummyColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)
        if 'catColumnName' in request.POST:
            catColumnName = request.POST['catColumnName']
            print('Categorical Column Name : {}'.format(catColumnName))
            df = create_categorical_column(get_selected_dataframe(request), catColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)
        if 'outlierColumnName' in request.POST:
            outlierColumnName = request.POST['outlierColumnName']
            print('outlier Column Name : {}'.format(outlierColumnName))
            df = remove_outlier(get_selected_dataframe(request), outlierColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)
        if 'lookoutlierColumnName' in request.POST:
            outlierColumnName = request.POST['lookoutlierColumnName']
            print('outlier Column Name : {}'.format(outlierColumnName))
            df = remove_outlier(get_selected_dataframe(request), outlierColumnName)
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)
        if 'dropnullrows' in request.POST:
            print('Dropping null rows')
            df = drop_null_rows(get_selected_dataframe(request))
            context = create_temp_context(request, df)
            return render(request, 'ops/data_prepare.html', context)
    else:
        selected_dataframe = get_selected_dataframe(request)
        # if type(selected_dataframe) == type(False):
        #     document_list = Document.objects.all()
        #     return render(request, 'ops/upload_file.html', {'documents': document_list})
        # else:

        context = create_temp_context(request, selected_dataframe)

        #let generate each chart for general view
        columns = selected_dataframe.columns
        temp_chart = {}
        for column in columns:
            chart = create_column_chart(selected_dataframe, column)
            temp_chart[column] = chart
            print('chart generated for : {}'.format(column))
        context['thumb_charts'] = temp_chart

        return render(request, 'ops/data_prepare.html', context)

def data_prepare_detail(request, pk):
    try:
        print('column : {}'.format(str(pk)))
        df = get_selected_dataframe(request)
    except Document.DoesNotExist:
        pass

    context = create_detail_context(request, get_selected_dataframe(request), pk)
    return render(request, 'ops/data_prepare.html', context)


def create_detail_context(request, df, pk):
    html = get_df_as_html(df,100)
    selected_column = df.columns[int(pk) - 1]

    column_describe = df[df.columns[int(pk)-1]].describe().to_dict()
    v_dtype_count = get_dtypes_as_dict(df)
    selected_column_type = v_dtype_count[selected_column]

    parameters = {}
    parameters['z'] = None
    parameters['chart_size_x'] = 4
    parameters['chart_size_y'] = 2
    parameters['chart-type'] = 'bar'
    parameters['chart_title'] = selected_column
    parameters['multiple-chart'] = False

    context = {'return_data': html,
        # 'files': request.session.get('files', False),
        'selected_column': str(selected_column),
        'selected_column_type': selected_column_type,
        'column_describe': column_describe,
        'v_dtype_count': v_dtype_count,
        'generated_chart': generate_column_image(get_selected_dataframe(request), 1, selected_column, **parameters),
        }
    return context


def create_column_chart(df, column_name):

    parameters = {}
    parameters['z'] = None
    parameters['chart_size_x'] = 2
    parameters['chart_size_y'] = 1
    parameters['chart-type'] = 'bar'
    parameters['multiple-chart'] = True
    return generate_column_image(df, 1, column_name, **parameters)

def get_selected_dataframe(request):
    try:
        document = Document.objects.get(is_active=True)
        return get_or_save_dataframe(document.pk)
    except:
        return False

def create_temp_context(request, df):

        html = get_df_as_html(df,100)

        context = {'return_data': html,
            # 'files': request.session.get('files', False),
            'v_null_counts': get_null_count(df),
            'v_zero_counts': get_zero_count(df),
            'v_duplicated_counts': get_duplicated_count(df),
            'v_row_count': get_row_count(df),
            'v_column_count': get_column_count(df),
            'v_dtype_count': get_dtypes_as_dict(df),
            }
        return context




class UploadFileView(View):
    def get(self, request):
        document_list = Document.objects.all()
        return render(self.request, 'ops/upload_file.html', {'documents': document_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            document = form.save()
            full_file_path = request.build_absolute_uri().replace('/file/new/', '') + document.file.url
            document.url = full_file_path
            document.save()
            data = {'is_valid': True, 'name': document.file.name, 'url': document.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)



def delete_document(request, pk):
    try:
        Document.objects.get(pk=pk).delete()
    except Document.DoesNotExist:
        pass
    document_list = Document.objects.all()
    return render(request, 'ops/upload_file.html', {'documents': document_list})

def delete_model(request, pk):
    try:
        ModelData.objects.get(pk=pk).delete()
    except ModelData.DoesNotExist:
        pass
    model_list = ModelData.objects.all()
    return render(request, 'ops/publish_model.html', {'model_list': model_list})



def toggle_status_model(request, pk):
    try:

        model = ModelData.objects.get(pk=pk)
        if(model.status):
            # Means model is reachable so kill port and disable
            model.status = False
            kill_pids(model.port)
            model.port = ''
            model.save()
        else:
            # Means model is not reachable so start model
            model.status = True
            port = find_free_port()
            start_model(model.model_path, port, model.ip)
            model.port = port
            model.save()

    except ModelData.DoesNotExist:
        pass
    model_list = ModelData.objects.all()
    return render(request, 'ops/publish_model.html', {'model_list': model_list})




def setactive_document(request, pk):
    try:
        documents  = Document.objects.all()
        for document in documents:
            document.is_active = False
            document.save()
        document = Document.objects.get(pk=pk)
        document.is_active = True
        document.save()
    except Document.DoesNotExist:
        pass
    document_list = Document.objects.all()
    return render(request, 'ops/upload_file.html', {'documents': document_list})


def get_current_document():
    try:
        return Document.objects.get(is_active=True)
    except:
        return False
