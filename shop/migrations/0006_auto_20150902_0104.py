# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150902_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='packs',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
