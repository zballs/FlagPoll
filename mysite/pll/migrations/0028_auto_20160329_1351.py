# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 18:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0027_auto_20160329_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 13, 51, 10, 83123)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 29, 13, 51, 10, 98748)),
        ),
    ]
