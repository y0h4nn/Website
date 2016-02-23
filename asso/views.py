import json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from . import models
from . import forms


@login_required
def index(request):
    context = {
        'assos': models.Asso.objects.all(),
    }
    return render(request, 'asso/index.html', context)


@login_required
def details(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    if asso.members_group:
        members = asso.members_group.user_set.select_related('profile').all()
    else:
        members = []
    context = {
        'asso': asso,
        'members': members,
        'user_is_admin': asso.user_is_admin(request.user),
    }
    return render(request, 'asso/details.html', context)


@login_required
def asso_members(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    if not asso.members_group:
        return JsonResponse({'users': []})
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
        } for user in asso.members_group.user_set.select_related('profile').all().only('id', 'first_name', 'last_name', 'username', 'profile', 'email')
    ]
    return JsonResponse({'users': users})


@permission_required('asso.manage_asso')
def asso_managment(request):
    context = {
        'assos': models.Asso.objects.all(),
    }
    return render(request, 'asso/managment.html', context)


@permission_required('asso.manage_asso')
def asso_settings(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    if request.method == 'POST':
        form = forms.AssoSettingsForm(request.POST, instance=asso)
        if form.is_valid():
            form.save()
            return redirect('asso:managment')
    else:
        form = forms.AssoSettingsForm(instance=asso)
    context = {
        'form': form,
        'asso': asso,
    }
    return render(request, 'asso/settings.html', context)


@permission_required('asso.manage_asso')
def asso_delete(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    asso.delete()
    return redirect('asso:managment')


@permission_required('asso.manage_asso')
def asso_create(request):
    if request.method == 'POST':
        form = forms.AssoSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asso:managment')
    else:
        form = forms.AssoSettingsForm()

    context = {
        'form': form,
    }
    return render(request, 'asso/create.html', context)


@login_required
def asso_edit(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    if not asso.user_is_admin(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = forms.AssoForm(request.POST, request.FILES, instance=asso)
        if form.is_valid():
            form.save()
            return redirect('asso:details', aid=asso.id)
    else:
        form = forms.AssoForm(instance=asso)

    context = {
        'form': form,
        'asso': asso,
        'user_is_admin': True,
    }
    return render(request, 'asso/edit.html', context)


@login_required
def asso_manage_members(request, aid):
    asso = get_object_or_404(models.Asso, pk=aid)
    if not asso.user_is_admin(request.user):
        raise PermissionDenied

    context = {
        'asso': asso,
        'user_is_admin': True,
    }
    if request.method == 'OPTIONS':
        json_data = json.loads(request.read().decode())
        if not json_data:
            admins = []
            members = []

            if asso.members_group:
                members = [u.username for u in asso.members_group.user_set.all().only('username')]

            if asso.admins_group:
                admins = [u.username for u in asso.admins_group.user_set.all().only('username')]

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
                    'is_member': user.username in members,
                    'is_admin': user.username in admins,
                } for user in User.objects.select_related('profile').all().only('id', 'first_name', 'last_name', 'username', 'profile', 'email')
            ]
            return JsonResponse({'users': users})
        if json_data.get('action') == 'add_member':
            try:
                user = User.objects.get(pk=json_data.get('uid'))
                user.groups.add(asso.members_group)
                return JsonResponse({})
            except User.DoesNotExist:
                return JsonResponse({'error': 'L\'utilisateur n\'existe pas'})
        if json_data.get('action') == 'del_member':
            try:
                user = User.objects.get(pk=json_data.get('uid'))
                user.groups.remove(asso.members_group)
                user.groups.remove(asso.admins_group)
                return JsonResponse({})
            except User.DoesNotExist:
                return JsonResponse({'error': 'L\'utilisateur n\'existe pas'})
        if json_data.get('action') == 'add_admin':
            try:
                user = User.objects.get(pk=json_data.get('uid'))
                user.groups.add(asso.admins_group)
                user.groups.add(asso.members_group)
                return JsonResponse({})
            except User.DoesNotExist:
                return JsonResponse({'error': 'L\'utilisateur n\'existe pas'})
        if json_data.get('action') == 'del_admin':
            try:
                user = User.objects.get(pk=json_data.get('uid'))
                user.groups.remove(asso.admins_group)
                return JsonResponse({})
            except User.DoesNotExist:
                return JsonResponse({'error': 'L\'utilisateur n\'existe pas'})
        return JsonResponse({'error': 'Action impossible'})

    return render(request, 'asso/manage_members.html', context)
