# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='semester',
            field=models.CharField(max_length=3, null=True, choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')], blank=True),
        ),
    ]
