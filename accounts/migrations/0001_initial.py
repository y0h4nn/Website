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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('street', models.CharField(null=True, max_length=512)),
                ('postal_code', models.IntegerField(null=True)),
                ('town', models.CharField(null=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('descriptionn', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(height_field='height', null=True, width_field='width', blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nickname', models.CharField(blank=True, null=True, max_length=255)),
                ('phone', models.CharField(blank=True, null=True, max_length=10)),
                ('picture', models.ImageField(blank=True, upload_to='profile_pictures', null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('enib_join_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('semester', models.CharField(blank=True, null=True, max_length=2, choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')])),
                ('family', models.ForeignKey(null=True, related_name='members', blank=True, to='accounts.Family')),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(height_field='height', null=True, width_field='width', blank=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='promo',
            field=models.ForeignKey(null=True, related_name='members', blank=True, to='accounts.Promo'),
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
            model_name='address',
            name='profile',
            field=models.OneToOneField(related_name='address', to='accounts.Profile'),
        ),
    ]
