from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.conf import settings

def bde_member(fnc):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse('accounts:login', next=request.path))

        bde_group = Group.objects.get(name=settings.BDE_GROUP_NAME)

        if bde_group not in request.user.groups.all() and not request.user.is_staff:
            return redirect(reverse('news:index'))

        return fnc(request, *args, **kwargs)
    return wrapper
