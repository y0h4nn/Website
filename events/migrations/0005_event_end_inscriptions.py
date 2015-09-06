# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_inscriptions',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 6, 16, 46, 18, 295032, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
