from . import models

def check_notifications(request):
    return {'user_have_notifications': models.Notification.has_notification(request.user) }
