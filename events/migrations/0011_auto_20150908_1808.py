# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_max_extern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, validators=[django.core.validators.MinValueValidator(0)], max_digits=19),
        ),
    ]
