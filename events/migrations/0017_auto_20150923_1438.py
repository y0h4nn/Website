# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_event_gestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='gestion',
            field=models.CharField(blank=True, null=True, max_length=3, default=None, choices=[(None, 'Pas de gestion'), ('WAF', 'Gestion style WAF'), ('NL', 'Gestion style no-limit')]),
        ),
    ]
