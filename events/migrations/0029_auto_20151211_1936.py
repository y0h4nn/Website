# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_event_photo_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo_path',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]