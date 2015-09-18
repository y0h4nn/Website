from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime


def next_weekday(d, weekday):
    ahead = weekday - d.weekday()
    while ahead <= 0:
        ahead += 7
    return d + datetime.timedelta(ahead)


class Command(models.Model):
    date = models.DateField()

    @classmethod
    def get_current(cls):
        try:
            last = cls.objects.latest('id')
            nex = next_weekday(timezone.now(), 2)
            if nex.date() != last.date:
                if nex.time() > datetime.time(hour=17, minute=30):
                    com = cls(date=nex)
                    com.save()
                    return com
                else:
                    return last
            else:
                return last
        except cls.DoesNotExist:
            nex = next_weekday(timezone.now(), 2)
            com = cls(date=nex)
            com.save()
            return com


class Pizza(models.Model):
    name = models.CharField(max_length=255, error_messages={'unique': 'Une pizza avec ce nom existe déjà'})
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Inscription(models.Model):
    command = models.ForeignKey(Command, related_name="inscriptions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pizza = models.ForeignKey(Pizza)

