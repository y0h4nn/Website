from django.shortcuts import render
from . import models
from . import forms


def index(request):
    return render(request, 'bde/index.html', {})


def contributors(request):
    return render(request, 'bde/contributors.html', {})
