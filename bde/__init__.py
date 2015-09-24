from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from .models import Contributor
from django.utils import timezone

def bde_member(fnc):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.path)

        if request.user.is_staff or request.user.groups.filter(name=settings.BDE_GROUP_NAME).count():
            return fnc(request, *args, **kwargs)

        return redirect(reverse('news:index'))
    return wrapper


def is_bde_member(user):
    if user.is_staff or user.groups.filter(name=settings.BDE_GROUP_NAME).count():
        return True
    else:
        return False


def is_contributor(user):
    try:
        return user.contribution.end_date >= timezone.now().date()
    except Contributor.DoesNotExist as e:
        return False
