# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebmailSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('webmail', models.CharField(null=True, choices=[(None, 'Toujours demander'), ('roundcube', 'Roundcube'), ('rainloop', 'Rainloop'), ('squirrel', 'Squirrel Mail'), ('horde', 'Horde')], default=None, max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='webmail_settings')),
            ],
        ),
    ]
