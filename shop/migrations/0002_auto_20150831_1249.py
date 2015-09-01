# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyinghistory',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='action',
            field=models.CharField(max_length=100, choices=[(None, 'Ne rien faire'), ('fullcontribution', 'Attribuer une cotisation complete'), ('halfcontribution', 'Attribuer une demi cotisation')], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
