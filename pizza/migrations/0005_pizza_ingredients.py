# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re


def migrate_data(apps, schema_editor):
    Pizza = apps.get_model('pizza', 'Pizza')
    for entry in Pizza.objects.all():
        m = re.search(r"(.+) \((.+)\)", entry.name)
        print(m)
        if m:
            entry.name = m.group(1)
            entry.ingredients = m.group(2)
            entry.save()
        else:
            print("Can't migrate", entry.name)
            entry.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0004_auto_20150918_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='ingredients',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RunPython(migrate_data),
        migrations.AlterField(
            model_name='pizza',
            name='ingredients',
            field=models.CharField(max_length=255, null=False),
        ),
    ]
