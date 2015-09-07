# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import uuid


def migrate_data(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    for entry in Event.objects.all():
        entry.uuid = uuid.uuid4()
        entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_extern',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(migrate_data),
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=django_extensions.db.fields.UUIDField(editable=False),
        )
    ]
