from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event, Inscription
from .forms import EventForm
import json


def index(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        event = get_object_or_404(Event, id=req['eid'])
        ins, created = Inscription.objects.get_or_create(event=event, user=request.user)
        if not created:
            ins.delete()
            return JsonResponse({'registered': 0})
        return JsonResponse({'registered': 1})
    context = {'events': Event.to_come(request.user)}
    return render(request, 'events/index.html', context)


def event(request, eid):
    return render(request, 'events/event.html')


def admin_index(request):
    context = {'events': Event.objects.all()}
    return render(request, 'events/admin/index.html', context)


def admin_add(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventForm()
    context = {'event_form': form}
    return render(request, 'events/admin/add.html', context)


def admin_view(request, eid):
    e = get_object_or_404(Event, id=eid)
    context = {'event': e}
    return render(request, 'events/admin/view.html', context)


def admin_edit(request, eid):
    e = get_object_or_404(Event, id=eid)
    form = EventForm(request.POST or None, instance=e)
    if form.is_valid():
        form.save()
    context = {'event': e, 'event_form': form}
    return render(request, 'events/admin/edit.html', context)


def admin_list_registrations(request, eid):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        event = get_object_or_404(Event, id=req['eid'])
        ins = Inscription.objects.get(event=event, user=request.user)
        ins.delete()
        return JsonResponse({"status": 1})
    e = get_object_or_404(Event, id=eid)
    reg = Inscription.objects.filter(event=e)
    return render(request, 'events/admin/list_registrations.html', {'event': e, 'reg': reg})

