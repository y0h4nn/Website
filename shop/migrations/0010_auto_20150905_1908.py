# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def migrate_data(apps, schema_editor):
    BuyingHistory = apps.get_model('shop', 'BuyingHistory')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    for entry in BuyingHistory.objects.all():
        user = User.objects.get(username=entry.username)
        entry.user = user
        entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20150905_1801'),
    ]

    operations = [
        migrations.AddField('BuyingHistory', 'user', models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True)),
        migrations.RunPython(migrate_data),
        migrations.AlterField('BuyingHistory', 'user', models.ForeignKey(settings.AUTH_USER_MODEL)),
        migrations.RemoveField('BuyingHistory', 'username'),
    ]
