from .forms import EventForm, ExternInscriptionForm
from .models import Event, Inscription, ExternInscription
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
import json
import csv
import uuid
from bde import bde_member


@login_required
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


@login_required
def event(request, eid):
    e = get_object_or_404(Event, id=eid)
    context = {'event': e}
    return render(request, 'events/event.html', context)


def event_extern(request, uuid):
    e = get_object_or_404(Event, uuid=uuid)
    if not e.allow_extern:
        return HttpResponse(status=404)
    if not e.places_left():
        return render(request, 'events/no_places.html')
    form = ExternInscriptionForm(request.POST or None, initial={"event": e})
    if form.is_valid():
        ins = form.save(commit=False)
        ins.event = e
        ins.save()
        return redirect('news:index')
    context = {'event': e, 'form': form}
    return render(request, 'events/event_extern.html', context)


@bde_member
def admin_index(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        event = get_object_or_404(Event, id=req['eid'])
        event.delete()
        return JsonResponse({"status": 1})
    context = {'events': Event.objects.all()}
    return render(request, 'events/admin/index.html', context)


@bde_member
def admin_list_events(request):
    if request.method == "OPTIONS":
        evts = Event.objects.all()
        return JsonResponse({'events': [{
            'eid': evt.id,
            'name': evt.name,
            'picture': evt.photo_url(),
            'start_time': evt.start_time,
            'deleted': False,
        } for evt in evts]})


@bde_member
def admin_add(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.uuid = uuid.uuid4()
            event.save()
            return redirect(reverse('events:admin_index'))
    else:
        form = EventForm()
    context = {'event_form': form}
    return render(request, 'events/admin/add.html', context)


@bde_member
def admin_edit(request, eid):
    e = get_object_or_404(Event, id=eid)
    form = EventForm(request.POST or None, request.FILES or None, instance=e)
    if form.is_valid():
        form.save()
        return redirect(reverse('events:admin_index'))
    context = {'event': e, 'event_form': form}
    return render(request, 'events/admin/edit.html', context)


@bde_member
def admin_list_registrations(request, eid):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        if 'iid' in req:
            if 'ext' not in req:
                ins = Inscription.objects.get(id=req['iid'])
                ins.delete()
            else:
                ins = ExternInscription.objects.get(id=req['iid'])
                ins.delete()
            return JsonResponse({"status": 1})
        return JsonResponse({"status": 0})
    e = get_object_or_404(Event, id=eid)
    reg = Inscription.objects.filter(event=e).select_related("user__profile").select_related('event')
    ext_reg = ExternInscription.objects.filter(event=e).select_related('event')
    return render(request, 'events/admin/list_registrations.html', {'event': e, 'reg': reg, 'ext_reg': ext_reg})


@bde_member
def admin_export_csv(request, eid):
    event = get_object_or_404(Event, id=eid)
    reg = Inscription.objects.filter(event=event).select_related("user__profile")
    ext_reg = ExternInscription.objects.filter(event=event)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(event.name)

    writer = csv.writer(response)
    writer.writerow(['Login', 'Surnom', 'Prénom', 'Nom', 'Mail'])
    for r in reg:
        line = [r.user.profile.user, r.user.profile.nickname, r.user.first_name, r.user.last_name, r.user.email]
        writer.writerow(line)
    for r in ext_reg:
        line = ["", "", r.first_name, r.last_name, r.mail]
        writer.writerow(line)
    return response
