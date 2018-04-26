# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 07:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('talkingtree', '0002_auto_20180426_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 7, 7, 9, 840621, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 7, 7, 9, 842088, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 7, 7, 9, 839902, tzinfo=utc)),
        ),
    ]