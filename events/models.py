from django.db import models
from django.conf import settings
from django.utils import timezone
from django.templatetags.static import static


class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(null=True, blank=True)

    def registrations_number(self):
        return len(self.inscriptions.all())

    def is_open(self):
        return self.start_date <= timezone.now() <= self.end_date

    def is_ended(self):
        return timezone.now() >= self.end_date

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('images/default_event_icon.png')

    def __str__(self):
        return self.name

    @staticmethod
    def to_come(user):
        return [(event.inscriptions.filter(user=user).count(), event) for event in Event.objects.filter(start_time__gt=timezone.now())]  # XXX: This mays be slow as hell, it needs some testing.


class Inscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="inscriptions")
    event = models.ForeignKey(Event, related_name="inscriptions")

    class Meta:
        unique_together = (('user', 'event'),)

