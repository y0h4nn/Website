# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0002_registration_is_simple_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='is_simple_comment',
            field=models.BooleanField(default=True),
        ),
    ]
