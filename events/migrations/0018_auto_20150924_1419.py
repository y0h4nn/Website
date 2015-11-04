# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20150923_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='externinscription',
            name='in_date',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='inscription',
            name='in_date',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='in_date',
            field=models.DateTimeField(null=True, default=None, blank=True),
        ),
    ]
