# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-09 02:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_user_drive_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='drive_code',
        ),
    ]