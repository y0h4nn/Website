from ..forms import ExternInscriptionForm, ExternLinkForm, InvitForm
from ..models import Event, Inscription, ExternLink, Invitation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

import json
import uuid


@login_required
def index(request):
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        event = get_object_or_404(Event, id=req['eid'])
        try:
            ins = Inscription.objects.get(event=event, user=request.user)
            ins.delete()
            return JsonResponse({'registered': 0, 'full': 0})
        except Inscription.DoesNotExist:
            if event.can_subscribe():
                ins = Inscription(event=event, user=request.user)
                ins.save()
                return JsonResponse({'registered': 1, 'full': 0})
            else:
                return JsonResponse({'registered': 0, 'full': 1})
    context = {'events': Event.to_come(request.user)}
    return render(request, 'events/index.html', context)


@login_required
def event(request, eid):
    e = get_object_or_404(Event, id=eid, model=False)
    context = {'event': e, 'links': [], 'user_can_invite': False}
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        inv = Invitation.objects.get(id=req['iid'], user=request.user)
        inv.delete()
        return JsonResponse({'status': 1})

    if e.allow_extern and request.user.has_perm('events.manage_event'):
        if request.method == "POST" and 'btn_link' in request.POST:
            form = ExternLinkForm(request.POST)
            if form.is_valid():
                link = form.save(commit=False)
                link.event = e
                link.uuid = uuid.uuid4()
                try:
                    link.save()
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, 'Un lien porte déjà ce nom.')
        else:
            form = ExternLinkForm()
        links = ExternLink.objects.filter(event=e)
        context['link_form'] = form
        context['links'] = links

    if e.can_invite(request.user):
        context['user_can_invite'] = True
        if request.method == "POST" and 'btn_invit' in request.POST:
            form = InvitForm(request.POST)
            if form.is_valid():
                ins = form.save(commit=False)
                ins.event = e
                ins.user = request.user
                try:
                    ins.save()
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, "Vous ne pouvez pas inviter 2 fois la meme personne avec la meme adresse email")
        else:
            form = InvitForm()
        context['invit_form'] = form
    context['invitations'] = e.invitations.filter(user=request.user)

    return render(request, 'events/event.html', context)


def event_extern(request, uuid):
    link = get_object_or_404(ExternLink, uuid=uuid)
    e = link.event
    if e.closed():
        return render(request, 'events/closed.html')
    if not link.places_left():
        return render(request, 'events/no_places.html')
    form = ExternInscriptionForm(request.POST or None, initial={"event": e})
    if form.is_valid():
        ins = form.save(commit=False)
        ins.event = e
        ins.via = link
        try:
            ins.save()
        except IntegrityError:
            messages.add_message(request, messages.WARNING, 'Vous êtes déjà inscrit à cet évènement')
        else:
            messages.add_message(request, messages.INFO, 'Vous avez bien été inscrit à l\'évènement')
        return redirect('news:index')
    context = {'event': e, 'form': form, 'link': link}
    return render(request, 'events/event_extern.html', context)

