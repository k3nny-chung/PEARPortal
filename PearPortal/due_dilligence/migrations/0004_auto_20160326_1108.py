# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import due_dilligence.models


class Migration(migrations.Migration):

    dependencies = [
        ('due_dilligence', '0003_auto_20160325_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='upload',
            field=models.FileField(editable=False, upload_to=due_dilligence.models.Document.doc_directory_path),
        ),
    ]
