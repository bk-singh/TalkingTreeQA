# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 11:02
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talkingtree', '0018_auto_20180417_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voteanswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.NullBooleanField(default=True)),
            ],
            options={
                'ordering': ['-vote'],
            },
        ),
        migrations.RemoveField(
            model_name='upvoteanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='upvoteanswer',
            name='user',
        ),
        migrations.AlterField(
            model_name='answer',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 17, 11, 2, 45, 421700)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 17, 11, 2, 45, 423182)),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 17, 11, 2, 45, 420906)),
        ),
        migrations.DeleteModel(
            name='Upvoteanswer',
        ),
        migrations.AddField(
            model_name='voteanswer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkingtree.Answer'),
        ),
        migrations.AddField(
            model_name='voteanswer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
