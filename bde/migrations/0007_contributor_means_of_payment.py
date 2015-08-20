# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bde', '0006_auto_20150818_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='means_of_payment',
            field=models.CharField(choices=[('cash', 'Espèces'), ('check', 'Chèque'), ('card', 'Carte')], max_length=5, default='cash'),
            preserve_default=False,
        ),
    ]
