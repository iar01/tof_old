# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0008_auto_20160214_0454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='audience_points',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='feed',
            name='total_points',
            field=models.FloatField(default=0),
        ),
    ]
