from django.shortcuts import render, redirect
from . import forms
from . import models

def index(request):
    context = {
        'albums': models.Album.objects.all()
    }
    return render(request, 'photo/index.html', context)


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
