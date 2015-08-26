# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
        migrations.AddField(
            model_name='notification',
            name='backref',
            field=models.CharField(max_length=255, default='notifications:index'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='backref_args',
            field=models.CharField(max_length=1024, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=255),
        ),
    ]
