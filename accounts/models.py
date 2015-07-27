from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


SEMESTERS = [(None, 'Aucun'),]
SEMESTERS += [('S{}'.format(i), 'Semestre {}'.format(i)) for i in range(1,11)]

class Family(models.Model):
    name = models.CharField(max_length=255)
    descriptionn = models.TextField(null=True, blank=True)
    picture = models.ImageField(height_field='height', width_field='width', null=True, blank=True)


class Promo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(height_field='height', width_field='width', null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    picture = models.ImageField(height_field='height', width_field='width', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    family = models.ForeignKey('Family', related_name='members', null=True, blank=True)
    promo = models.ForeignKey('Promo', related_name='members', null=True, blank=True)
    enib_join_year = models.PositiveSmallIntegerField(null=True, blank=True)
    semester = models.CharField(max_length=2, choices=SEMESTERS, null=True, blank=True)

    def __str__(self):
        return self.nickname


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

