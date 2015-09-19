import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User, Permission


def list_perms(request_json, user):
    perms = Permission.objects.all()

    response = {
        'perms': {},
        'staff': user.is_staff,
    }
    for perm in perms:
        if perm.content_type.app_label not in response['perms']:
            response['perms'][perm.content_type.app_label] = []

        response['perms'][perm.content_type.app_label].append({
            'name': perm.name,
            'codename': perm.codename,
            'state': user.has_perm("%s.%s" % (perm.content_type.app_label, perm.codename)),
        })
    return JsonResponse(response)

def set_perm(request_json, user):
    perm = Permission.objects.get(codename=request_json.get('codename'))
    codename = request_json.get('codename')
    state = request_json.get('state')

    if perm is None or state is None or codename is None:
        return JsonResponse({'error': 'Missing arguments'})

    full_codename = "%s.%s" % (perm.content_type.app_label, perm.codename)
    if user.has_perm(full_codename) and not state:
        user.user_permissions.remove(perm)
        print("removed perm")
    elif not user.has_perm(full_codename) and state:
        user.user_permissions.add(perm)
        print("added perm")
    user.save()

    return JsonResponse({})

ACTIONS = {
    'list': list_perms,
    'set': set_perm,
}

def index(request):
    context = {}


    if request.method == 'OPTIONS':
        req = json.loads(request.read().decode())
        user = get_object_or_404(User, id=req.get('uid'))
        if req.get('action') in ACTIONS:
            return ACTIONS[req.get('action')](req, user)

    return render(request, 'permissions/index.html', context)

