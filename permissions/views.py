import json
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import permission_required, login_required
from .forms import GroupCreationForm


class ActionRouter:
    def __init__(self, request):
        self._request = request
        self.request = json.loads(request.read().decode())

    def route(self):
        """
        Do not catch errors so debug stay simple.
        """
        action = self.request.get('action')
        return self.__getattribute__(action)()


class UserActionRouter(ActionRouter):
    def __init__(self, request):
        super().__init__(request)
        self.user = get_object_or_404(User, id=self.request.get('uid'))

    def list_perms(self):
        perms = Permission.objects.all()
        response = {
            'perms': [],
            'groups': [{
                    'id': g.id,
                    'name': g.name,
                    'color': '#%s' % (hashlib.md5(g.name.encode()).hexdigest()[:6]),
                } for g in self.user.groups.all()],
        }
        for perm in perms:
            app_label = perm.content_type.app_label
            if settings.PERM_ENABLE_WHITELIST:
                if app_label not in settings.PERM_WHITELIST:
                    continue
                if perm.codename not in settings.PERM_WHITELIST[app_label]:
                    continue

            response['perms'].append({
                'section': perm.content_type.app_label,
                'name': perm.name,
                'codename': perm.codename,
                'state': self.user.has_perm("%s.%s" % (perm.content_type.app_label, perm.codename)),
                'enabled': "%s.%s" % (perm.content_type.app_label, perm.codename) not in self.user.get_group_permissions() and not self.user.is_superuser,
            })
            response['perms'].sort(key=lambda p: p['section'])
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


class GroupActionRouter(ActionRouter):
    GROUP_DELETION_BLACKLIST = [
        'Enib',
        'Tous',
        settings.BDE_GROUP_NAME,
    ]

    def __init__(self, request):
        super().__init__(request)
        self.group = get_object_or_404(Group, id=self.request.get('gid'))

    def list_perms(self):
        perms = Permission.objects.all()
        group_perms = self.group.permissions.all()
        response = {
            'perms': [],
        }
        for perm in perms:
            app_label = perm.content_type.app_label
            if app_label not in settings.PERM_WHITELIST:
                continue
            if perm.codename not in settings.PERM_WHITELIST[app_label]:
                continue

            response['perms'].append({
                'section': perm.content_type.app_label,
                'name': perm.name,
                'codename': perm.codename,
                'state': perm in group_perms,
                'enabled': True,
            })
            response['perms'].sort(key=lambda p: p['section'])
        return JsonResponse(response)

    def set_perm(self):
        perm = Permission.objects.get(codename=self.request.get('codename'))
        group_perms = self.group.permissions.all()
        codename = self.request.get('codename')
        state = self.request.get('state')

        if perm is None or state is None or codename is None:
            return JsonResponse({'error': 'Missing arguments'})

        full_codename = "%s.%s" % (perm.content_type.app_label, perm.codename)
        if perm in group_perms and not state:
            self.group.permissions.remove(perm)
        elif perm not in group_perms and state:
            self.group.permissions.add(perm)
        self.group.save()
        return JsonResponse({})

    def add_user(self):
        try:
            user = User.objects.get(id=self.request.get('uid'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'L\'utilisateur n\'existe pas.'})

        user.groups.add(self.group)
        return JsonResponse({})

    def del_user(self):
        try:
            user = User.objects.get(id=self.request.get('uid'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'L\'utilisateur n\'existe pas.'})

        user.groups.remove(self.group)
        return JsonResponse({})

    def remove(self):
        if not self._request.user.has_perm('auth.delete_group'):
            return JsonResponse({'error': 'Droit insufisants'})
        if self.group.name not in self.GROUP_DELETION_BLACKLIST:
            self.group.delete()
            return JsonResponse({})
        else:
            return JsonResponse({'error': 'Ce groupe n\'est pas supprimable'})


@permission_required('auth.change_permission')
def users(request):
    context = {}
    if request.method == 'OPTIONS':
        router = UserActionRouter(request)
        return router.route()
    return render(request, 'permissions/users.html', context)


@permission_required('auth.change_permission')
def groups(request):
    if request.method == 'OPTIONS':
        router = GroupActionRouter(request)
        fuckdat = router.route()
        if fuckdat is not None:
            return fuckdat
        else:
            return JsonResponse({'error': 'Action invalide'})

    elif request.method == 'POST':
        if request.user.has_perm('auth.add_group'):
            form = GroupCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('permissions:groups')
        else:
            messages.add_message(request, messages.ERROR, 'Vous n\'avez pas les droits pour créer un groupe.')

    form = GroupCreationForm()
    return render(request, 'permissions/groups.html', {'form': form})


@login_required
def custom_member_list(request, gid):
    group = get_object_or_404(Group, id=gid)
    users = [
        {
            'id': user.id,
            'display_name': str(user.profile),
            'picture': user.profile.get_picture_url(),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'nickname': user.profile.nickname,
            'email': user.email,
            'in_group': group in user.groups.all(),
        } for user in User.objects.select_related('profile').prefetch_related('groups').all()
    ]
    return JsonResponse({'users': users})
