# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 01:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20170629_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='data',
            new_name='Image',
        ),
    ]
