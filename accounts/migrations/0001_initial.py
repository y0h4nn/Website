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
                ('street', models.CharField(blank=True, null=True, max_length=512)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('town', models.CharField(blank=True, null=True, max_length=255)),
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
                ('descriptionn', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(height_field='height', upload_to='', blank=True, null=True, width_field='width')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nickname', models.CharField(blank=True, null=True, max_length=255)),
                ('phone', models.CharField(blank=True, null=True, max_length=10)),
                ('picture', models.ImageField(upload_to='profile_pictures', blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('enib_join_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('semester', models.CharField(choices=[(None, 'Aucun'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2'), ('S3', 'Semestre 3'), ('S4', 'Semestre 4'), ('S5', 'Semestre 5'), ('S6', 'Semestre 6'), ('S7', 'Semestre 7'), ('S8', 'Semestre 8'), ('S9', 'Semestre 9'), ('S10', 'Semestre 10')], blank=True, null=True, max_length=2)),
                ('family', models.ForeignKey(related_name='members', to='accounts.Family', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(height_field='height', upload_to='', blank=True, null=True, width_field='width')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='promo',
            field=models.ForeignKey(related_name='members', to='accounts.Promo', blank=True, null=True),
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
