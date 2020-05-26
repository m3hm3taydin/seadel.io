from django.contrib import admin

from django.urls import include, path, re_path
from django_registration.backends.one_step.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static

from core.views import IndexTemplateView

from users.forms import CustomUserForm


urlpatterns = [
    path('accounts/register/', RegistrationView.as_view(form_class=CustomUserForm, success_url='/'), name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include('users.api.urls')),
    # re_path(r'^$', views.IndexView.as_view(), name='index'),
    # re_path(r'^datasource/$', views.DataSourceView.as_view(), name='data_source'),
    # re_path(r'^file/download/$', views.send_file, name='download'),
    # re_path(r'^prepare/$', views.data_prepare, name='data_prepare'),
    # re_path(r'^prepare/(?P<pk>\d+)/$', views.data_prepare_detail, name='data_prepare_detail'),

    # re_path(r'^file/ops/(?P<operation>[\w-]+)/$', views.modal_show, name='null_modal'),


    # re_path(r'^file/new/$', views.UploadFileView.as_view(), name='upload'),

    # re_path(r'^visualize/$', views.visualize_data, name='visualize_data'),
    # re_path(r'^visualize/generate_chart$', views.generate_chart, name='generate_chart'),


    # re_path(r'^analyse/$', views.analyse_data, name='analyse_data'),
    # re_path(r'^analyse/prediction/$', views.analyse_prediction, name='analyse_prediction'),
    # re_path(r'^analyse/prediction/auto$', views.analyse_prediction_auto, name='analyse_prediction_auto'),
    # re_path(r'^analyse/clustering/$', views.analyse_clustering, name='analyse_clustering'),

    # re_path(r'^publish/$', views.publish_model, name='publish_model'),

    # re_path(r'^document/file_settings/$', views.file_settings, name='file_settings'),

    # re_path(r'^document/delete/(?P<pk>\d+)/$', views.delete_document, name='delete_document'),
    # re_path(r'^model/delete/(?P<pk>\d+)/$', views.delete_model, name='delete_model'),
    # re_path(r'^document/setactive/(?P<pk>\d+)/$', views.setactive_document, name='setactive_document'),

    # re_path(r'^model/status/(?P<pk>\d+)/$', views.toggle_status_model, name='toggle_status_model'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

urlpatterns +=  re_path(r'^.*$', IndexTemplateView.as_view(), name='entry-path'),


# handler404 = views.error_404
# handler500 = views.error_500
