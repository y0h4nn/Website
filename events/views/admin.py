from ..forms import EventForm, RecurrentEventForm, RecurrentEventEditForm, FormulaFormSet
from ..models import Event, Inscription, ExternInscription, Invitation, RecurrentEvent, Formula

from django.conf import settings
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from bde.shortcuts import is_contributor

import csv
import json
import os
import os.path
import uuid


@user_passes_test(lambda u: u.has_module_perms('events'))
def admin_index(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        event = get_object_or_404(Event, id=req['eid'])
        event.delete()
        return JsonResponse({"status": 1})
    context = {'events': Event.objects.all()}
    return render(request, 'events/admin/index.html', context)


@user_passes_test(lambda u: u.has_module_perms('events'))
def admin_list_events(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        if req['arg'] == "new":
            evts = Event.objects.filter(start_time__gt=timezone.now(), model=False).order_by('start_time')
        else:
            evts = Event.objects.filter(start_time__lt=timezone.now(), model=False).order_by('start_time').reverse()
        return JsonResponse({'events': [{
            'eid': evt.id,
            'name': evt.name,
            'picture': evt.photo_url(),
            'start_time': evt.start_time,
            'deleted': False,
        } for evt in evts]})


@permission_required('events.manage_event')
def admin_add(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES or None)
        fform = FormulaFormSet(request.POST, queryset=Formula.objects.none())
        if form.is_valid():
            event = form.save(commit=False)
            event.uuid = uuid.uuid4()
            event.save()
            if fform.is_valid():
                formulas = fform.save(commit=False)
                for formula in formulas:
                    formula.event = event
                    formula.save()
            return redirect(reverse('events:admin_index'))
    else:
        form = EventForm()
        fform = FormulaFormSet(queryset=Formula.objects.none())
    autocomplete_dirs = []
    realpath = os.path.join(settings.MEDIA_ROOT, 'photo')
    for root, dirs, files in os.walk(os.path.join(realpath)):
        for d in dirs:
            autocomplete_dirs.append(os.path.relpath(os.path.join(root, d), start=realpath))
    context = {'event_form': form,
               'autocomplete_dirs': autocomplete_dirs,
               'formula_form': fform,
               }
    return render(request, 'events/admin/add.html', context)


@permission_required('events.manage_recurrent_event')
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


@permission_required('events.manage_recurrent_event')
def admin_edit_recurrent(request, eid):
    e = get_object_or_404(RecurrentEvent, id=eid, model=True)
    form = RecurrentEventEditForm(request.POST or None, request.FILES or None, instance=e)
    if form.is_valid():
        if not form.cleaned_data['allow_invitations']:
            Invitation.objects.filter(event=e).delete()
        form.save()
        return redirect(reverse('events:admin_recurrent'))
    context = {'event': e, 'event_form': form}
    return render(request, 'events/admin/recurrent_edit.html', context)


@permission_required('events.manage_recurrent_event')
def admin_del_recurrent(request, eid):
    e = get_object_or_404(RecurrentEvent, id=eid, model=True)
    e.delete()
    return redirect('events:admin_recurrent')


@permission_required('events.manage_recurrent_event')
def admin_recurrent(request):
    context = {'events': RecurrentEvent.objects.all()}
    return render(request, 'events/admin/recurrent_index.html', context)


@permission_required('events.manage_event')
def admin_edit(request, eid):
    e = get_object_or_404(Event, id=eid, model=False)
    form = EventForm(request.POST or None, request.FILES or None, instance=e)
    fform = FormulaFormSet(request.POST or None, queryset=e.formulas.all())
    if form.is_valid():
        if not form.cleaned_data['allow_invitations']:
            Invitation.objects.filter(event=e).delete()
        event = form.save()
        if fform.is_valid():
            formulas = fform.save(commit=False)
            for formula in formulas:
                formula.event = event
                formula.save()
        return redirect(reverse('events:admin_index'))
    autocomplete_dirs = []
    realpath = os.path.join(settings.MEDIA_ROOT, 'photo')
    for root, dirs, files in os.walk(os.path.join(realpath)):
        for d in dirs:
            autocomplete_dirs.append(os.path.relpath(os.path.join(root, d), start=realpath))

    context = {'event': e, 'event_form': form, 'formula_form': fform, "autocomplete_dirs": autocomplete_dirs}
    return render(request, 'events/admin/edit.html', context)


@permission_required('events.access_list')
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
    reg = Inscription.objects.filter(event=e).select_related("user__profile").select_related('event').select_related('formula')
    ext_reg = ExternInscription.objects.filter(event=e).select_related('event').select_related('via').select_related('formula')
    invits = Invitation.objects.filter(event=e).select_related('event').select_related('user__profile').select_related('formula')
    return render(request, 'events/admin/list_registrations.html', {'event': e, 'reg': reg, 'ext_reg': ext_reg, 'invits': invits})


@permission_required('events.access_list')
def admin_export_csv(request, eid):
    event = get_object_or_404(Event, id=eid, model=False)
    reg = Inscription.objects.filter(event=event).select_related("user__profile").select_related("user__contribution")
    ext_reg = ExternInscription.objects.filter(event=event).select_related("via")
    invits = Invitation.objects.filter(event=event).select_related('user__profile')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(event.name)

    writer = csv.writer(response)

    def formula_price(formula, contributor=False):
        if formula is None:
            return 0
        if contributor:
            p = formula.price_contributor
        else:
            p = formula.price_non_contributor
        return "{} €".format(p)

    writer.writerow(['Login', 'Surnom', 'Prénom', 'Nom', 'Mail', 'From', 'Entrée', 'Externe', 'Formule', "Cotisant", "Prix", "Moyen de paiement"])
    for r in reg:
        contributor = is_contributor(r.user)
        line = [r.user.profile.user, r.user.profile.nickname, r.user.first_name, r.user.last_name, r.user.email, "ENIB", r.in_date, '0', r.formula, contributor, formula_price(r.formula, contributor) if r.formula else event.price, r.payment_mean]
        writer.writerow(line)
    for r in ext_reg:
        line = ["", "", r.first_name, r.last_name, r.mail, r.via.name, r.in_date, '1', r.formula, False, formula_price(r.formula) if r.formula else event.price, r.payment_mean]
        writer.writerow(line)
    for r in invits:
        line = ["", "", r.first_name, r.last_name, r.mail, str(r.user.profile), r.in_date, '1', r.formula, False, formula_price(r.formula) if r.formula else event.price, r.payment_mean]
        writer.writerow(line)
    return response

