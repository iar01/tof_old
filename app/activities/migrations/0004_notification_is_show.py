# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_remove_activity_competitions_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_show',
            field=models.BooleanField(default=False),
        ),
    ]
