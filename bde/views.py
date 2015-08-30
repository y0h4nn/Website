import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
from . import models
from . import forms
from . import bde_member


def index(request):
    return render(request, 'bde/index.html', {})


@bde_member
def contributors(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        if not req.get('user'):
            return JsonResponse({'error': 'Requette invalide. Contactez votre sysadmin.'})

        user = User.objects.get(id=req.get('user'))
        if not user:
            return JsonResponse({'error': 'Utilisateur inconu. Contactez votre sysadmin.'})

        valid_actions = [
            'half_contribution_add',
            'half_contribution_delete',
            'full_contribution_add',
            'full_contribution_delete',
        ]

        if req.get('action') not in valid_actions:
            return JsonResponse({'error': 'Action inconue. Contactez votre sysadmin'})

        if req.get('action').endswith('delete'):
            try:
                user.contribution.delete()
                return JsonResponse({'error': None})
            except models.Contributor.DoesNotExist:
                return JsonResponse({'error': 'L\'utilisateur n\'est pas cotisant'})

        elif req.get('action') == 'half_contribution_add':
            now = datetime.datetime.now()
            if 1 <= now.month <= 6:
                endate = datetime.date(now.year, 6, 30)
            else:
                endate = datetime.date(now.year, 12, 31)
            contrib_type = 'half'

        elif req.get('action') == 'full_contribution_add':
            now = datetime.datetime.now()
            if 8 <= now.month <= 12:
                endate = datetime.date(now.year + 1, 6, 30)
                contrib_type = 'full'
            else:
                return JsonResponse({'error': 'La fulll cotiz ne peux plus être prise pour l\'année en cours'})
        else:
            return JsonResponse({'error': 'Stop envoyer de la merde. Contactez votre sysadmin.'})

        models.Contributor.objects.update_or_create({
            'end_date': endate,
            'type': contrib_type,
            'means_of_payment': req.get('mean'),
        }, user=user)

        return JsonResponse({'error': None})
    return render(request, 'bde/contributors.html', {})

@bde_member
def detail(request, id):
    user = User.objects.get(id=id);

    try:
        for mean in models.MEANS_OF_PAYMENT:
            if mean[0] == user.contribution.means_of_payment:
                mean_name = mean[1]

        context = {
            'user': user,
            'username': str(user.profile),
            'start': user.contribution.start_date,
            'end': user.contribution.end_date,
            'mean': mean_name
        }
    except models.Contributor.DoesNotExist:
        context = {
            'user': user,
            'username': str(user.profile),
            'error': True
        }

    return render(request, 'bde/contributors_detail.html', context)

@bde_member
def members(request):
    context = {}

    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())

        try:
            user = User.objects.get(id=req.get('user'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur inconu. Contactez votre sysadmin.'})

        try:
            group = Group.objects.get(name=settings.BDE_GROUP_NAME)
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Impossible de trouver le group du bde. Contactez votre administrateur systeme'})

        if req.get('action') == 'add':
            user.groups.add(group)
        elif req.get('action') == 'delete':
            user.group.remove(group)
            pass
        else:
            return JsonResponse({'error': 'Action inconue'})

        return JsonResponse({'error': None})

    return render(request, 'bde/members.html', context)


@bde_member
def memberlist(request):
    bde_group = Group.objects.get(name=settings.BDE_GROUP_NAME)
    users = [
        {
            'id': user.id,
            'display_name': str(user.profile),
            'picture': user.profile.get_picture_url(),
            'profile_url': user.profile.get_url(),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'nickname': user.profile.nickname,
            'email': user.email,
            'is_member': bde_group in user.groups.all(),
        } for user in User.objects.select_related('profile').all()
    ]
    return JsonResponse({'users': users})
