# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150913_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='limited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='max_inscriptions',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=0),
        ),
    ]
