# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('parent', models.ForeignKey(default=None, blank=True, to='photo.Album', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(upload_to='', width_field='width', height_field='height')),
                ('Album', models.ForeignKey(to='photo.Album')),
            ],
        ),
    ]
