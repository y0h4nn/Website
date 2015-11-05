import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User, Permission


class ActionRouter:
    def __init__(self, request):
        self.request = json.loads(request.read().decode())

    def route(self):
        try:
            action = self.request.get('action')
            return self.__getattribute__(action)()
        except (AttributeError, TypeError):
            return None


class UserActionRouter(ActionRouter):
    def __init__(self, request):
        super().__init__(request)
        self.user = get_object_or_404(User, id=self.request.get('uid'))

    def list_perms(self):
        perms = Permission.objects.all()
        response = {
            'perms': {},
            'superuser': self.user.is_superuser,
        }
        for perm in perms:
            if perm.content_type.app_label not in response['perms']:
                response['perms'][perm.content_type.app_label] = []

            response['perms'][perm.content_type.app_label].append({
                'name': perm.name,
                'codename': perm.codename,
                'state': self.user.has_perm("%s.%s" % (perm.content_type.app_label, perm.codename)),
            })
        return JsonResponse(response)

    def set_perm(self):
        perm = Permission.objects.get(codename=self.request.get('codename'))
        codename = self.request.get('codename')
        state = self.request.get('state')

        if perm is None or state is None or codename is None:
            return JsonResponse({'error': 'Missing arguments'})

        full_codename = "%s.%s" % (perm.content_type.app_label, perm.codename)
        if self.user.has_perm(full_codename) and not state:
            self.user.user_permissions.remove(perm)
        elif not self.user.has_perm(full_codename) and state:
            self.user.user_permissions.add(perm)
        self.user.save()
        return JsonResponse({})

    def set_superuser(self):
        if self.request.get('superuser'):
            self.user.is_superuser = True
        else:
            self.user.is_superuser = False
        self.user.save()
        return self.list_perms()

def users(request):
    context = {}
    if request.method == 'OPTIONS':
        router = UserActionRouter(request)
        return router.route()
    return render(request, 'permissions/users.html', context)


def groups(request):
    if request.method == 'OPTIONS':
        router = GroupActionRouter(request)
        return router.route()
    return render(request, 'permissions/groups.html')

