# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 16:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0023_auto_20160327_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='tag',
            field=models.CharField(choices=[('Postal', 'Postal'), ('Infrastructure', 'Infrastructure')], default='no tag', max_length=30),
        ),
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 27, 11, 13, 50, 499057)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 27, 11, 13, 50, 501559)),
        ),
    ]
