# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20150901_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packs',
            name='products',
            field=models.ManyToManyField(to='shop.Product', blank=True),
        ),
    ]
