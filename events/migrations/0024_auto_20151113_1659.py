# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2015-11-13 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_event_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurrentevent',
            name='last_created',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
