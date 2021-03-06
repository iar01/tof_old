# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitions', '0009_competition_finish_upload_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='cash_prize',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='judge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='competition',
            name='judge_about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='rulez',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='scoring_criteria',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='theme',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
