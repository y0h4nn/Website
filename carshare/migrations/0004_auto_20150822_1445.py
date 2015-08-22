# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carshare', '0003_auto_20150822_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='annoucement',
            new_name='announcement',
        ),
    ]
