# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-13 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0012_remove_document_words'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='words',
            field=models.CharField(max_length=200, null=True),
        ),
    ]