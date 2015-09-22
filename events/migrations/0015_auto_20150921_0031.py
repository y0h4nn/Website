# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0014_auto_20150920_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('mail', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('event', models.ForeignKey(to='events.Event', related_name='invitations')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='invitations')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('mail', 'event')]),
        ),
    ]
