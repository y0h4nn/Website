# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150817_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
