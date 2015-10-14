import os
from django.shortcuts import render, redirect
from . import forms
from . import models

PHOTO_ROOT="/home/arnaud/Desktop/Images"
ALLOWED_IMAGE_EXT = ['.jpg', '.jpeg', '.png']

def list_albums(path):
    albums = []

    for f in os.listdir(path):
        if not os.path.isdir(os.path.join(path, f)):
            continue
        albums.append(f)

    return albums


def list_images(path):
    images = []

    for f in os.listdir(path):
        if not os.path.isfile(os.path.join(path, f)):
            continue
        if os.path.splitext(f)[1] not in ALLOWED_IMAGE_EXT:
            print("%s is not an allowed format" % os.path.splitext(f)[1])
            continue
        images.append(f)

    return images


def browse(request, path):
    realpath = os.path.join(PHOTO_ROOT, path)
    if not os.path.isdir(realpath):
        return redirect('photo:browse', path='')

    print(realpath)

    context = {
        'path': realpath,
        'albums': list_albums(realpath),
        'images': list_images(realpath),
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
