from . import models

def notify(user, title, message):
    models.Notification.objects.create(user=user, title=title, message=message)
