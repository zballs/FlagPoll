# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-29 20:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0037_auto_20160429_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 15, 47, 56, 228676)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 15, 47, 56, 234180)),
        ),
    ]
