# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 02:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0042_auto_20160514_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 21, 26, 24, 471412)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 21, 26, 24, 487036)),
        ),
    ]