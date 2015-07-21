from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


SEMESTERS = [(None, 'Aucun'),]
SEMESTERS += [('S{}'.format(i), 'Semestre {}'.format(i)) for i in range(1,11)]

class Family(models.Model):
    name = models.CharField(max_length=255)
    descriptionn = models.TextField()
    picture = models.ImageField(height_field='height', width_field='width')


class Promo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(height_field='height', width_field='width')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=255)
    picture = models.ImageField(height_field='height', width_field='width')
    birthdate = models.DateField()
    family = models.ForeignKey('Family', related_name='members')
    promo = models.ForeignKey('Promo', related_name='members')
    enib_join_year = models.PositiveSmallIntegerField()
    semester = models.CharField(max_length=2, choices=SEMESTERS, default=None)


class Email(models.Model):
    email = models.EmailField()
    profile = models.ForeignKey('Profile', related_name='secondary_emails')
    valid = models.BooleanField(default=False)


class Adress(models.Model):
    profile = models.ForeignKey('Profile', related_name='addresses')
    name = models.CharField(max_length=255)
    description = models.TextField()
    street = models.TextField()
    postal_code = models.IntegerField()
    town = models.CharField(max_length=255)
    contry = models.CharField(max_length=255)

