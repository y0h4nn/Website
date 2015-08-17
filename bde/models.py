from django.db import models
from django.conf import settings

class Contributor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    paid = models.BooleanField(default=False)
