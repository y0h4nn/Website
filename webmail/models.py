from django.db import models
from django.conf import settings

WEBMAILS = [
    (None, 'Toujours demander'),
    ('roundcube', 'Roundcube'),
    ('rainloop', 'Rainloop'),
    ('squirrel', 'Squirrel Mail'),
    ('horde', 'Horde'),
]

class WebmailSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="webmail_settings")
    webmail = models.CharField(max_length=50, choices=WEBMAILS, null=True, default=None, blank=True)
