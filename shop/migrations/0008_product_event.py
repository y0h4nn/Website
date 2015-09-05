# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150817_1136'),
        ('shop', '0007_auto_20150902_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='event',
            field=models.ForeignKey(to='events.Event', null=True, blank=True),
        ),
    ]
