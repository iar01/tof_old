# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0008_auto_20151222_1246'),
        ('feeds', '0003_auto_20151221_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='competition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competitions.Competition'),
        ),
    ]
