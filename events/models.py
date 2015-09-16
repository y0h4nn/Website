from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.templatetags.static import static
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=255)
    end_inscriptions = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    photo = models.ImageField(null=True, blank=True)
    private = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)
    max_inscriptions = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    allow_extern = models.BooleanField(default=False)

    def registrations_number(self):
        return self.inscriptions.all().count() + self.extern_inscriptions.all().count()

    def can_subscribe(self):
        return not self.limited or self.inscriptions.all().count() < self.max_inscriptions

    def is_open(self):
        return self.start_date <= timezone.now() <= self.end_date

    def is_ended(self):
        return timezone.now() >= self.end_date

    def closed(self):
        return timezone.now() >= self.end_inscriptions

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('images/default_event_icon.png')

    def __str__(self):
        return self.name

    @staticmethod
    def to_come(user):
        return [(event.inscriptions.filter(user=user).count(), event) for event in Event.objects.filter(
            Q(end_inscriptions__gt=timezone.now()),
            Q(inscriptions__user=user) | Q(private=False)
        ).distinct()]


class ExternLink(models.Model):
    event = models.ForeignKey(Event, related_name="extern_links")
    uuid = models.UUIDField()
    maximum = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = (('name', 'event'),)

    def places_left(self):
        return self.maximum > self.inscriptions.all().count()


class Inscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="inscriptions")
    event = models.ForeignKey(Event, related_name="inscriptions")

    class Meta:
        unique_together = (('user', 'event'),)


class ExternInscription(models.Model):
    mail = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, related_name="extern_inscriptions")
    via = models.ForeignKey(ExternLink, related_name="inscriptions")

    class Meta:
        unique_together = (('mail', 'event'),)

