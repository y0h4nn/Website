from django.shortcuts import render


def event(request, eid):
    return render(request, 'events/event.html')
