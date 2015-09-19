from django.conf import settings
from django.db import models
from django.utils import timezone


class Command(models.Model):
    date = models.DateTimeField()

    @classmethod
    def get_current(cls):
        try:
            return cls.objects.latest('id')
        except cls.DoesNotExist:
            return None

    def is_valid(self):
        try:
            return self.date > timezone.now()
        except:
            return False


class Pizza(models.Model):
    name = models.CharField(max_length=255, error_messages={'unique': 'Une pizza avec ce nom existe déjà'})
    ingredients = models.CharField(max_length=255, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.name, self.ingredients)


class Inscription(models.Model):
    command = models.ForeignKey(Command, related_name="inscriptions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pizza = models.ForeignKey(Pizza)

