# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20150913_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_invitations',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='max_invitations',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='event',
            name='max_invitations_by_person',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
