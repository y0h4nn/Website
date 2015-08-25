from django.db import models
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    message = models.TextField()

    @staticmethod
    def has_notification(user):
        return Notification.objects.filter(user=user,read=False).count() > 0
