# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 19:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0007_auto_20160322_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 22, 14, 55, 58, 333629)),
        ),
    ]