# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 18:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0026_auto_20160329_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 13, 12, 42, 240671)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 13, 12, 42, 240671)),
        ),
    ]
