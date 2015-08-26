from . import models

def check_notifications(request):
    if request.user.is_active:
        has = models.Notification.has_notification(request.user)
    else:
        has = False
    return {'user_have_notifications':  has}
