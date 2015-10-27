import os
import PIL
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.db import IntegrityError
from . import forms
from . import models
from bde.shortcuts import bde_member

# photo directory name
PHOTO_DIRNAME = "photo"
THUMBNAIL_DIRNAME = '.thumbnails'
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png']



def create_thumbnail(realpath, filename):
    if not os.path.isdir(os.path.join(realpath, THUMBNAIL_DIRNAME)):
        os.mkdir(os.path.join(realpath, THUMBNAIL_DIRNAME))

    if os.path.isfile(os.path.join(realpath, THUMBNAIL_DIRNAME, filename)):
        return

    image = PIL.Image.open(os.path.join(realpath, filename))

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


def user_can_access(user, path):
    if user.is_superuser:
        return True

    policies = models.AccessPolicy.list(path)
    access = False
    for p in policies:
        access |= p.user_can_access(user)
    return access


def list_entries(realpath, path, user):
    entries = {
        'files': [],
        'dirs': [],
    }

    for entry in os.scandir(realpath):
        if entry.is_dir():
            if entry.name != THUMBNAIL_DIRNAME:
                if user_can_access(user, os.path.join(path, entry.name)):
                    entries['dirs'].append({
                        'name': entry.name,
                        'path': os.path.join(path, entry.name),
                    })
        elif entry.is_file():
            if os.path.splitext(entry.name)[1].lower() in ALLOWED_IMAGE_EXT:
                entries['files'].append({
                    'name': entry.name,
                    'path': os.path.join(settings.MEDIA_URL, PHOTO_DIRNAME, path, entry.name),
                    'thumbnail': os.path.join(settings.MEDIA_URL, PHOTO_DIRNAME, path, THUMBNAIL_DIRNAME, entry.name),
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
    if path and not user_can_access(request.user, path):
        raise Http404

    entries = list_entries(realpath, path, request.user)
    context = {
        'path': path,
        'parent': os.path.normpath(os.path.join(path, '..')),
        'albums': entries['dirs'],
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
                    pass

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
    return redirect('photo:permissions', path=path)

