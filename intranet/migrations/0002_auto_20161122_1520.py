# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-22 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.BooleanField(default=True),
        ),
    ]