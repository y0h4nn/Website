import os
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.conf import settings
from django.db import IntegrityError
from . import forms
from . import models
from bde.shortcuts import bde_member, is_bde_member

# photo directory name
PHOTO_DIRNAME = "photo"
THUMBNAIL_DIRNAME = '.thumbnails'
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png']



def create_thumbnail(realpath, filename):
    if not os.path.isdir(os.path.join(realpath, THUMBNAIL_DIRNAME)):
        os.mkdir(os.path.join(realpath, THUMBNAIL_DIRNAME))

    if os.path.isfile(os.path.join(realpath, THUMBNAIL_DIRNAME, filename)):
        return

    try:
        image = Image.open(os.path.join(realpath, filename))
        l = min(image.size)
        width, height = image.size
        box = (
            int((width - l) / 2),
            int((height - l) / 2),
            int((width + l) / 2),
            int((height + l) / 2)
        )
        region = image.crop(box)
        region.thumbnail((100,100))
        region.save(os.path.join(realpath, THUMBNAIL_DIRNAME, filename), "JPEG")
    except OSError:
        return


def can_access(path, user=None, email=None):
    if user and (user.is_superuser or is_bde_member(user)):
        return True

    policies = models.AccessPolicy.list(path)
    access = False
    for p in policies:
        access |= p.user_can_access(user) or p.extern_can_access(email)
    return access


def list_entries(realpath, path, user=None, email=None):
    entries = {
        'files': [],
        'dirs': [],
    }

    for entry in os.scandir(realpath):
        if entry.is_dir():
            if entry.name != THUMBNAIL_DIRNAME:
                if can_access(os.path.join(path, entry.name), user, email):
                    entries['dirs'].append({
                        'name': entry.name,
                        'path': os.path.join(path, entry.name),
                    })
        elif entry.is_file():
            if os.path.splitext(entry.name)[1].lower() in ALLOWED_IMAGE_EXT:
                entries['files'].append({
                    'name': entry.name,
                    'path': os.path.join(
                        settings.MEDIA_URL,
                        PHOTO_DIRNAME,
                        path,
                        entry.name
                    ),
                    'thumbnail': os.path.join(
                        settings.MEDIA_URL,
                        PHOTO_DIRNAME,
                        path,
                        THUMBNAIL_DIRNAME,
                        entry.name
                    ),
                })
                create_thumbnail(realpath, entry.name)

    return entries


def browse(request, path):
    realpath = os.path.join(settings.MEDIA_ROOT, PHOTO_DIRNAME, path)
    if not os.path.normpath(realpath).startswith(os.path.join(settings.MEDIA_ROOT, PHOTO_DIRNAME)):
        raise Http404
    if not os.path.isdir(realpath):
        raise Http404
    if os.path.basename(realpath).startswith('.'):
        raise Http404

    email = request.session.get('email')
    user = request.user if request.user.is_authenticated() else None
    if path and not can_access(path, user, email):
        if user:
            raise Http404
        else:
            return redirect('photo:extern_login', next=path)

    entries = list_entries(realpath, path, user, email)
    context = {
        'path': path,
        'parent': os.path.normpath(os.path.join(path, '..')),
        'albums': sorted(entries['dirs'], key=lambda x: x['name'].lower()),
        'images': entries['files'],
    }

    return render(request, 'photo/browse.html', context)


@bde_member
def permissions(request, path):
    form_instances = []

    if request.method == 'POST':
        if request.POST.get('selected_form') in forms.get_forms():
            instance = forms.get_forms()[request.POST.get('selected_form')](request.POST)
            if instance.is_valid():
                try:
                    policy = instance.save(commit=False)
                    policy.path = path
                    policy.save()
                    instance.save()
                except IntegrityError:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "Cette permission est déjà en place."
                    )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Impossible d'ajouter cette permission. Veuillez remplir tous les champs."
                )

        return redirect(request.path)

    else:
        for name, form in forms.get_forms().items():
            form_instances.append({
                'name': name,
                'description': form.__doc__,
                'instance': form()
            })


    context = {
        'path': path,
        'forms': form_instances,
        'permissions': models.AccessPolicy.list(path),
    }
    return render(request, 'photo/permissions.html', context)

@bde_member
def permissions_delete(request, model, pid):
    model_classes = models.get_models()
    if model in model_classes:
        cls = model_classes[model]
        policy = get_object_or_404(cls, pk=pid)
        path = policy.path
        policy.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "La permission a été révoquée."
        )
    return redirect('photo:permissions', path=path)


def extern_login(request, next):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        return redirect('photo:browse', path=next)
    else:
        return render(request, 'photo/extern_login.html')
