# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webmail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webmailsettings',
            name='webmail',
            field=models.CharField(max_length=50, blank=True, default=None, choices=[(None, 'Toujours demander'), ('roundcube', 'Roundcube'), ('rainloop', 'Rainloop'), ('squirrel', 'Squirrel Mail'), ('horde', 'Horde')], null=True),
        ),
    ]
