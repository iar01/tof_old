# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 22:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feed',
            old_name='photo_id',
            new_name='image_url',
        ),
    ]
