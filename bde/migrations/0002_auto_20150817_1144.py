# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bde', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contributor',
            old_name='end_dtae',
            new_name='end_date',
        ),
    ]
