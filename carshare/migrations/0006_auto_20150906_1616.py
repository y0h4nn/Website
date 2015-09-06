# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0005_auto_20150906_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='status',
            field=models.CharField(null=True, default=None, max_length=8, choices=[(None, 'En attente'), ('accepted', 'Acceptée'), ('refused', 'Refusée')]),
        ),
    ]
