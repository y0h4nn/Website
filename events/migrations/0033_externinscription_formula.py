# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_invitation_formula'),
    ]

    operations = [
        migrations.AddField(
            model_name='externinscription',
            name='formula',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extern_inscriptions', to='events.Formula'),
        ),
    ]
