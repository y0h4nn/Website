# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('username', models.CharField(max_length=80)),
                ('product', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('payment_mean', models.CharField(max_length=10, choices=[('cash', 'Espèces'), ('check', 'Chèque'), ('card', 'Carte de crédit')])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('action', models.CharField(null=True, blank=True, max_length=100, choices=[(None, 'Ne rien faire'), ('fullcontribution', 'Attribuer une contisation complete'), ('halfcontribution', 'Attribuer une demi cotisation')])),
            ],
        ),
    ]
