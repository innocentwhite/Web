# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-10 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import upload.models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0012_auto_20170710_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='project',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='picture',
            name='Image',
            field=models.ImageField(upload_to=upload.models.upload_to_path),
        ),
    ]
