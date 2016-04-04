# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='uploads/documents/')),
                ('category', models.CharField(max_length=50)),
                ('type', models.BooleanField()),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('abstract', models.CharField(max_length=200)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
