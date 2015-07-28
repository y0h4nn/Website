# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('street', models.TextField()),
                ('postal_code', models.IntegerField()),
                ('town', models.CharField(max_length=255)),
                ('contry', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('descriptionn', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(upload_to='', width_field='width', height_field='height', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nickname', models.CharField(max_length=255, blank=True, null=True)),
                ('picture', models.ImageField(upload_to='', width_field='width', height_field='height', blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('enib_join_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('semester', models.CharField(max_length=2, choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')], blank=True, null=True)),
                ('family', models.ForeignKey(blank=True, to='accounts.Family', related_name='members', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(upload_to='', width_field='width', height_field='height', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='promo',
            field=models.ForeignKey(blank=True, to='accounts.Promo', related_name='members', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='email',
            name='profile',
            field=models.ForeignKey(to='accounts.Profile', related_name='secondary_emails'),
        ),
        migrations.AddField(
            model_name='adress',
            name='profile',
            field=models.ForeignKey(to='accounts.Profile', related_name='addresses'),
        ),
    ]
