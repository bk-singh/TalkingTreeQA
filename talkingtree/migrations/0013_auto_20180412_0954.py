# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-12 09:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talkingtree', '0012_auto_20180412_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 9, 54, 34, 599786)),
        ),
    ]
