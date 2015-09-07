# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150907_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternInscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('event', models.ForeignKey(to='events.Event', related_name='extern_inscriptions')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='externinscription',
            unique_together=set([('mail', 'event')]),
        ),
    ]
