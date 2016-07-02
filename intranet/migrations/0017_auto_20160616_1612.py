# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-16 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0016_auto_20160513_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='doi',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='issn',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.CharField(max_length=50, null=True),
        ),
    ]