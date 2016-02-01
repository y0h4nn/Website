from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    backref = models.CharField(max_length=255)
    backref_args = models.CharField(max_length=1024)

    class Meta:
        app_label = 'notifications'

    @staticmethod
    def has_notification(user):
        return Notification.objects.filter(user=user, read=False).count() > 0

    def backref_url(self):
        if self.backref_args:
            kwargs = dict([arg.split('=') for arg in self.backref_args.split(';')])
            return reverse(self.backref, kwargs=kwargs)
        else:
            return reverse(self.backref)

