# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-15 02:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pll', '0041_auto_20160430_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='glyph',
            field=models.CharField(default='no glyph', max_length=30),
        ),
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 21, 19, 42, 434937)),
        ),
        migrations.AlterField(
            model_name='voice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 21, 19, 42, 440439)),
        ),
    ]