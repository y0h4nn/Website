# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0004_auto_20150822_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='status',
            field=models.CharField(null=True, choices=[(None, 'En attente'), ('refused', 'Refusée'), ('accepted', 'Acceptée')], default=None, max_length=8),
        ),
    ]
