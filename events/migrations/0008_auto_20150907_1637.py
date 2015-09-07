# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150907_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(),
        ),
    ]
