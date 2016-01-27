# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def migrate(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DELETE FROM pizza_command")
        cursor.execute("DELETE FROM pizza_inscription")


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0003_auto_20150918_2233'),
    ]

    operations = [
        migrations.RunPython(migrate),
    ]
