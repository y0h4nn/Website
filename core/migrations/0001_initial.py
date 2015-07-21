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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('descriptionn', models.TextField()),
                ('picture', models.ImageField(width_field='width', height_field='height', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nickname', models.CharField(max_length=255)),
                ('picture', models.ImageField(width_field='width', height_field='height', upload_to='')),
                ('birthdate', models.DateField()),
                ('enib_join_year', models.PositiveSmallIntegerField()),
                ('semester', models.CharField(default=None, max_length=2, choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')])),
                ('family', models.ForeignKey(related_name='members', to='core.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('picture', models.ImageField(width_field='width', height_field='height', upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='promo',
            field=models.ForeignKey(related_name='members', to='core.Promo'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='email',
            name='profile',
            field=models.ForeignKey(related_name='secondary_emails', to='core.Profile'),
        ),
        migrations.AddField(
            model_name='adress',
            name='profile',
            field=models.ForeignKey(related_name='addresses', to='core.Profile'),
        ),
    ]
