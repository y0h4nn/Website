# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bde', '0004_auto_20150818_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='contributions'),
        ),
    ]
