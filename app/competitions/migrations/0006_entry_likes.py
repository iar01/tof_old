# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0005_auto_20151220_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='likes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
