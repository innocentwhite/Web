# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-08 06:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0009_auto_20170629_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='uploader',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
