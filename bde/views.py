from django.shortcuts import render


def index(request):
    return render(request, 'bde/index.html', {})


def contributors(request):
    return render(request, 'bde/contributors.html', {})
