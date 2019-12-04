from django.db import models

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    document_url = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    seperator = models.CharField(max_length=10, default=",")
    row_count = models.IntegerField(default=0)
    header_row = models.IntegerField(default=0)
    encoding = models.CharField(max_length=20, default="utf-8")
    updated = models.IntegerField(default=0)

class ModelData(models.Model):
    model_path = models.CharField(max_length=255, blank=True)
    sample_path = models.CharField(max_length=255, blank=True)
    selected_models = models.CharField(max_length=255, blank=True)
    auc = models.CharField(max_length=255, blank=True)
    logloss = models.CharField(max_length=255, blank=True)
    mean_per_class_error = models.CharField(max_length=255, blank=True)
    rmse = models.CharField(max_length=255, blank=True)
    mse = models.CharField(max_length=255, blank=True)
    ip = models.CharField(max_length=255, blank=True)
    port = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Next Feature
# Will be recorded all transactions to this model
class TransactionData(models.Model):
    query = models.CharField(max_length=1000, blank=False)
    query_status = models.BooleanField(default=False)
    runned_by = models.CharField(max_length=255, default="")
    query_startdate = models.DateTimeField(auto_now_add=True)
    query_enddate = models.DateTimeField(auto_now_add=True)
    data_file = models.CharField(max_length=255, blank=True)
    pickle_file = models.CharField(max_length=255, blank=True)
    document_pk = models.IntegerField(default=0, blank=False)
    prev_trans_pk = models.IntegerField(blank=False)
