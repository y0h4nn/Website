from . import models


class ReadOnVisit:
    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        notifications = models.Notification.objects.filter(
            user=request.user,
            read=False
        )
        for notification in notifications:
            if notification.backref_url() == request.path:
                notification.read = True
                notification.save()
