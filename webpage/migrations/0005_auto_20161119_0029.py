# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-19 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0004_news_admin_annotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='header',
            field=models.FileField(max_length=500, null=True, upload_to='static/webpage/images/news/header/'),
        ),
        migrations.AddField(
            model_name='news',
            name='mini_description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='thumbnail',
            field=models.FileField(max_length=500, null=True, upload_to='static/webpage/images/news/thumbnail/'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
