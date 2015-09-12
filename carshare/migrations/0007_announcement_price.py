# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0006_auto_20150906_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='price',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
