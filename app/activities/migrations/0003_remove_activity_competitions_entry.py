# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 11:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activity_competitions_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='competitions_entry',
        ),
    ]
