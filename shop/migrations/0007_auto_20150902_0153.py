# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def delete_history(apps, schema_editor):
    BuyingHistory = apps.get_model("shop", "BuyingHistory")
    BuyingHistory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20150902_0104'),
    ]

    operations = [
        migrations.RunPython(delete_history)
    ]
