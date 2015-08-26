from django.contrib.auth.models import Group
from . import models

def notify(message, backref, backref_args=None, users=None, groups=None):
    targets = []

    for group in groups or []:
        targets += [u for u in group.users]

    if users is not None:
        targets += users

    if backref_args:
        backref_args_str = ';'.join(["%s=%s" % (k,v) for k,v in backref_args.items()])
    else:
        backref_args_str = ""

    for user in targets:
        models.Notification.objects.create(
            user=user,
            message=message,
            backref=backref,
            backref_args=backref_args_str,
        )
