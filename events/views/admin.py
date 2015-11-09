from ..forms import EventForm, RecurrentEventForm
from ..models import Event, Inscription, ExternInscription, Invitation, RecurrentEvent
from bde.shortcuts import bde_member

from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

import csv
import json
import uuid


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
        req = json.loads(request.read().decode())
        if req['arg'] == "new":
            evts = Event.objects.filter(start_time__gt=timezone.now(), model=False).order_by('start_time').reverse()
        else:
            evts = Event.objects.filter(start_time__lt=timezone.now(), model=False).order_by('start_time').reverse()
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
def admin_add_recurrent(request):
    if request.method == "POST":
        form = RecurrentEventForm(request.POST, request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.uuid = uuid.uuid4()
            event.model = True
            event.save()
            return redirect(reverse('events:admin_recurrent'))
    else:
        form = RecurrentEventForm()
    context = {'event_form': form}
    return render(request, 'events/admin/recurrent_add.html', context)


@bde_member
def admin_edit_recurrent(request, eid):
    e = get_object_or_404(RecurrentEvent, id=eid, model=True)
    form = RecurrentEventForm(request.POST or None, request.FILES or None, instance=e)
    if form.is_valid():
        if not form.cleaned_data['allow_invitations']:
            Invitation.objects.filter(event=e).delete()
        form.save()
        return redirect(reverse('events:admin_recurrent'))
    context = {'event': e, 'event_form': form}
    return render(request, 'events/admin/recurrent_edit.html', context)


@bde_member
def admin_del_recurrent(request, eid):
    e = get_object_or_404(RecurrentEvent, id=eid, model=True)
    e.delete()
    return redirect('events:admin_recurrent')


@bde_member
def admin_recurrent(request):
    context = {'events': RecurrentEvent.objects.all()}
    return render(request, 'events/admin/recurrent_index.html', context)



@bde_member
def admin_edit(request, eid):
    e = get_object_or_404(Event, id=eid, model=False)
    form = EventForm(request.POST or None, request.FILES or None, instance=e)
    if form.is_valid():
        if not form.cleaned_data['allow_invitations']:
            Invitation.objects.filter(event=e).delete()
        form.save()
        return redirect(reverse('events:admin_index'))
    context = {'event': e, 'event_form': form}
    return render(request, 'events/admin/edit.html', context)


@bde_member
def admin_list_registrations(request, eid):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        if 'iid' in req:
            if 'ext' in req:
                ins = ExternInscription.objects.get(id=req['iid'])
            elif 'inv' in req:
                ins = Invitation.objects.get(id=req['iid'])
            else:
                ins = Inscription.objects.get(id=req['iid'])
            ins.delete()
            return JsonResponse({"status": 1})
        return JsonResponse({"status": 0})
    e = get_object_or_404(Event, id=eid, model=False)
    reg = Inscription.objects.filter(event=e).select_related("user__profile").select_related('event')
    ext_reg = ExternInscription.objects.filter(event=e).select_related('event')
    invits = Invitation.objects.filter(event=e).select_related('event').select_related('user__profile')
    return render(request, 'events/admin/list_registrations.html', {'event': e, 'reg': reg, 'ext_reg': ext_reg, 'invits': invits})


@bde_member
def admin_export_csv(request, eid):
    event = get_object_or_404(Event, id=eid, model=False)
    reg = Inscription.objects.filter(event=event).select_related("user__profile")
    ext_reg = ExternInscription.objects.filter(event=event).select_related("via")
    invits = Invitation.objects.filter(event=event).select_related('user__profile')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(event.name)

    writer = csv.writer(response)
    writer.writerow(['Login', 'Surnom', 'Prénom', 'Nom', 'Mail', 'From'])
    for r in reg:
        line = [r.user.profile.user, r.user.profile.nickname, r.user.first_name, r.user.last_name, r.user.email, "ENIB"]
        writer.writerow(line)
    for r in ext_reg:
        line = ["", "", r.first_name, r.last_name, r.mail, r.via.name]
        writer.writerow(line)
    for r in invits:
        line = ["", "", r.first_name, r.last_name, r.mail, str(r.user.profile)]
        writer.writerow(line)
    return response

