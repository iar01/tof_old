# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-09 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_feed_judge_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='share_points',
            field=models.IntegerField(default=0),
        ),
    ]
