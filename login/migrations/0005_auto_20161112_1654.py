# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-12 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_user_drive_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='career',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=80, null=True),
        ),
    ]