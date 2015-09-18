# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_auto_20150916_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
