from django.db import models
from django.conf import settings

CONTRIBUTION_TYPES = [
    ('half', 'Demi-cotisation'),
    ('full', 'Cotisation'),
]

class Contributor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="contribution")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    type = models.CharField(max_length=4, choices=CONTRIBUTION_TYPES) 
