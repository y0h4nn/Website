# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150907_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_extern',
            field=models.IntegerField(default=0),
        ),
    ]
