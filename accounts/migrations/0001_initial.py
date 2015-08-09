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
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('street', models.TextField(null=True, blank=True)),
                ('postal_code', models.IntegerField(null=True, blank=True)),
                ('town', models.CharField(null=True, max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('descriptionn', models.TextField(null=True, blank=True)),
                ('picture', models.ImageField(height_field='height', null=True, upload_to='', width_field='width', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nickname', models.CharField(null=True, max_length=255, blank=True)),
                ('picture', models.ImageField(null=True, upload_to='profile_pictures', blank=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('enib_join_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('semester', models.CharField(choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')], null=True, max_length=2, blank=True)),
                ('family', models.ForeignKey(related_name='members', null=True, blank=True, to='accounts.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('picture', models.ImageField(height_field='height', null=True, upload_to='', width_field='width', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='promo',
            field=models.ForeignKey(related_name='members', null=True, blank=True, to='accounts.Promo'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='email',
            name='profile',
            field=models.ForeignKey(related_name='secondary_emails', to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='address',
            name='profile',
            field=models.OneToOneField(related_name='address', to='accounts.Profile'),
        ),
    ]
