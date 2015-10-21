import os
import PIL
from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from . import forms
from . import models

PHOTO_ROOT = "photo"
THUMBNAIL_DIRNAME = '.thumbnails'
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png']



def create_thumbnail(realpath, filename):
    if not os.path.isdir(os.path.join(realpath, THUMBNAIL_DIRNAME)):
        os.mkdir(os.path.join(realpath, THUMBNAIL_DIRNAME))

    if os.path.isfile(os.path.join(realpath, THUMBNAIL_DIRNAME, filename)):
        return

    image = PIL.Image.open(os.path.join(realpath, filename))
    image.thumbnail((100,100))
    image.save(os.path.join(realpath, THUMBNAIL_DIRNAME, filename), "JPEG")


def user_can_access(user, path):
    if user.is_superuser:
        return True

    policies = models.AccessPolicy.list(path)
    print("Bleh", policies)
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
            if os.path.splitext(entry.name)[1] in ALLOWED_IMAGE_EXT:
                entries['files'].append({
                    'name': entry.name,
                    'path': os.path.join('medias', PHOTO_ROOT, path, entry.name),
                    # TODO FIXME XXX
                    'thumbnail': os.path.join('medias', PHOTO_ROOT, path, THUMBNAIL_DIRNAME, entry.name),
                })
                create_thumbnail(realpath, entry.name)

    return entries


def browse(request, path):
    realpath = os.path.join(settings.MEDIA_ROOT, PHOTO_ROOT, path)
    if not os.path.normpath(realpath).startswith(os.path.join(settings.MEDIA_ROOT, PHOTO_ROOT)):
        raise Http404
    if not os.path.isdir(realpath):
        raise Http404
    if os.path.basename(realpath).startswith('.'):
        raise Http404

    entries = list_entries(realpath, path, request.user)
    context = {
        'path': path,
        'parent': os.path.normpath(os.path.join(path, '..')),
        'albums': entries['dirs'],
        'images': entries['files'],
    }

    return render(request, 'photo/browse.html', context)


def permissions(request, path):
    form_instances = []

    if request.method == 'POST':
        for name, form in forms.POLICIES_FORMS.items():
            instance = form(request.POST)
            if instance.has_changed() and instance.is_valid():
                policy = instance.save(commit=False)
                policy.path = path
                policy.save()
                instance.save()

        return redirect(request.path)

    else:
        for name, form in forms.POLICIES_FORMS.items():
            form_instances.append({
                'name': name,
                'instance': form()
            })


    context = {
        'path': path,
        'forms': form_instances,
        'permissions': models.AccessPolicy.list(path),
    }
    return render(request, 'photo/permissions.html', context)


def add_album(request):
    if request.method == 'POST':
        form = forms.AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('photo:index')

    else:
        form = forms.AlbumForm()

    context = {
        'form': form
    }
    return render(request, 'photo/add_album.html', context)
