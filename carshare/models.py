from django.db import models
from django.conf import settings
from collections import OrderedDict

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    destination = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    places = models.PositiveSmallIntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='carshares')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title

    def available_places(self):
        return self.places - Registration.objects.filter(models.Q(announcement=self) & models.Q(status='accepted') & ~models.Q(is_simple_comment=True)).count()


REGISTRATION_STATUS = OrderedDict([
    (None, 'En attente'),
    ('accepted', 'Acceptée'),
    ('refused', 'Refusée'),
])

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    announcement = models.ForeignKey(Announcement)
    status = models.CharField(max_length=8, null=True, choices=REGISTRATION_STATUS.items())
    is_simple_comment = models.BooleanField(default=True)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def status_name(self):
        return REGISTRATION_STATUS[self.status]

