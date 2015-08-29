from django.contrib.auth.models import Group
from django.conf import settings

def bde_member(request):
    bde_group = Group.objects.get(name=settings.BDE_GROUP_NAME)
    if bde_group in request.user.groups.all() or request.user.is_staff:
        return {'user_is_bde_member': True}
    else:
        return {'user_is_bde_member': False}

