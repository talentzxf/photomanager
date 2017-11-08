# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_path', models.CharField(max_length=200)),
                ('md5', models.CharField(max_length=33)),
                ('modified_time', models.DateTimeField(verbose_name='Date Modified')),
            ],
        ),
    ]
