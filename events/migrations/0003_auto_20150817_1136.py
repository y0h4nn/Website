# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150815_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(upload_to='', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inscription',
            name='user',
            field=models.ForeignKey(related_name='inscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]
