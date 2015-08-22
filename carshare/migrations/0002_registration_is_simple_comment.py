# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_simple_comment',
            field=models.BooleanField(default=False),
        ),
    ]
