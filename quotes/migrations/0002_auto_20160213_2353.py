# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-13 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prof',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
