import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError
from . import models
from . import forms


def index(request):
    return render(request, 'bde/index.html', {})


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
            'type': contrib_type
        }, user=user)

        return JsonResponse({'error': None})
    return render(request, 'bde/contributors.html', {})
