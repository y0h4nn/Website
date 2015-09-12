# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150908_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('uuid', models.UUIDField()),
                ('maximum', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_extern',
        ),
        migrations.RemoveField(
            model_name='event',
            name='uuid',
        ),
        migrations.AddField(
            model_name='externlink',
            name='event',
            field=models.ForeignKey(related_name='extern_links', to='events.Event'),
        ),
        migrations.AddField(
            model_name='externinscription',
            name='via',
            field=models.ForeignKey(default=-1, related_name='inscriptions', to='events.ExternLink'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='externlink',
            unique_together=set([('name', 'event')]),
        ),
    ]
