# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bde', '0002_auto_20150817_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='paid',
        ),
        migrations.AddField(
            model_name='contributor',
            name='type',
            field=models.CharField(max_length=4, default='full', choices=[('half', 'Demi-cotisation'), ('full', 'Cotisation')]),
            preserve_default=False,
        ),
    ]
