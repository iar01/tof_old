# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0013_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='comp',
        ),
        migrations.RemoveField(
            model_name='result',
            name='comp_feed',
        ),
        migrations.AlterField(
            model_name='competition',
            name='status',
            field=models.CharField(choices=[('n', 'not calculated'), ('y', 'calculated')], default='n', max_length=1),
        ),
        migrations.DeleteModel(
            name='result',
        ),
    ]