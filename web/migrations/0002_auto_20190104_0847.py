# Generated by Django 2.1.2 on 2019-01-04 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_row_count',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='document',
            name='file_seperator',
            field=models.CharField(default=',', max_length=2),
        ),
    ]
