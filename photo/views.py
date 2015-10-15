import os
from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from . import forms
from . import models

PHOTO_ROOT="photo"
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png']

def list_entries(realpath, path):
    entries = {
        'files': [],
        'dirs': [],
    }

    for entry in os.scandir(realpath):


        if entry.is_dir():
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
                })

    return entries


def browse(request, path):
    realpath = os.path.join(settings.MEDIA_ROOT, PHOTO_ROOT, path)
    if not os.path.normpath(realpath).startswith(os.path.join(settings.MEDIA_ROOT, PHOTO_ROOT)):
        raise Http404
    if not os.path.isdir(realpath):
        raise Http404

    entries = list_entries(realpath, path)
    context = {
        'path': path,
        'parent': os.path.normpath(os.path.join(path, '..')),
        'albums': entries['dirs'],
        'images': entries['files'],
    }

    return render(request, 'photo/browse.html', context)


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
