# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_feed_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='image_url',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='video_url',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
