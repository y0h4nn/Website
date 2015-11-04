# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150921_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='gestion',
            field=models.CharField(default=None, max_length=3, choices=[(None, 'Pas de gestion'), ('WAF', 'Gestion style WAF'), ('NL', 'Gestion style no-limit')], null=True),
        ),
    ]
