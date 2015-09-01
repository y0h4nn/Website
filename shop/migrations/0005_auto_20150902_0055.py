# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20150901_2349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyinghistory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='buyinghistory',
            name='price',
        ),
        migrations.AddField(
            model_name='buyinghistory',
            name='pack',
            field=models.ForeignKey(default=None, null=True, to='shop.Packs'),
        ),
        migrations.AddField(
            model_name='buyinghistory',
            name='type',
            field=models.CharField(max_length=10, default='produit', choices=[('product', 'Produit'), ('pack', 'Pack')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyinghistory',
            name='product',
            field=models.ForeignKey(default=None, null=True, to='shop.Product'),
        ),
    ]
