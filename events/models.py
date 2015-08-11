from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(height_field='height', width_field='width', null=True, blank=True)


class Inscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.ForeignKey(Event, related_name="inscriptions")

