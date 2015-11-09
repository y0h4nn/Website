from .forms import EventForm, ExternInscriptionForm, ExternLinkForm, InvitForm
from .models import Event, Inscription, ExternInscription, ExternLink, Invitation
from bde.shortcuts import is_contributor
from shop.models import BuyingHistory
from django.db.models import Count

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.templatetags.static import static

import csv
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
    e = get_object_or_404(Event, id=eid)
    context = {'event': e, 'links': [], 'user_can_invite': False}
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        inv = Invitation.objects.get(id=req['iid'], user=request.user)
        inv.delete()
        return JsonResponse({'status': 1})

    if e.allow_extern and request.user.has_perm('events.change_event'):
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
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Vous ne pouvez pas inviter 2 fois la meme personne avec la meme adresse email"
                    )
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
            evts = Event.objects.filter(start_time__gt=timezone.now()).order_by('start_time').reverse()
        else:
            evts = Event.objects.filter(start_time__lt=timezone.now()).order_by('start_time').reverse()
        return JsonResponse({'events': [{
            'eid': evt.id,
            'name': evt.name,
            'picture': evt.photo_url(),
            'start_time': evt.start_time,
            'deleted': False,
        } for evt in evts]})


@permission_required('events.add_event')
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


@permission_required('events.change_event')
def admin_edit(request, eid):
    e = get_object_or_404(Event, id=eid)
    form = EventForm(request.POST or None, request.FILES or None, instance=e)
    if form.is_valid():
        if not form.cleaned_data['allow_invitations']:
            Invitation.objects.filter(event=e).delete()
        form.save()
        return redirect(reverse('events:admin_index'))
    context = {'event': e, 'event_form': form}
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
    e = get_object_or_404(Event, id=eid)
    reg = Inscription.objects.filter(event=e).select_related("user__profile").select_related('event')
    ext_reg = ExternInscription.objects.filter(event=e).select_related('event')
    invits = Invitation.objects.filter(event=e).select_related('event').select_related('user__profile')
    return render(request, 'events/admin/list_registrations.html', {'event': e, 'reg': reg, 'ext_reg': ext_reg, 'invits': invits})


@permission_required('events.access_list')
def admin_export_csv(request, eid):
    event = get_object_or_404(Event, id=eid)
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

@permission_required('events.manage_entries')
def admin_management(request, eid):
    event = get_object_or_404(Event, id=eid)
    if event.gestion is None:
        raise Http404

    context = {'event': event}

    return render(request, 'events/admin/management_index.html', context)

@permission_required('events.manage_entries')
def management_list_users(request, eid):
    e = get_object_or_404(Event, id=eid)
    ret = {}
    if request.method == "OPTIONS":
        # Reg
        ret['reg'] = [{
                "display_name": str(ins.user.profile),
                "picture": ins.user.profile.get_picture_url(),
                "color": "bg-blue" if ins.in_date is not None else "bg-green" if is_contributor(ins.user) else "bg-red",
                "type": "reg",
                "id": ins.id,
            } for ins in Inscription.objects.filter(event=e).select_related("user__profile").select_related('event').select_related("user__contribution").annotate(null_nick=Count('user__profile__nickname')).order_by('null_nick', '-user__profile__nickname', '-user__last_name', '-user__first_name', '-user__username').reverse()
        ]
        ret['ext_reg'] = [{
                "display_name": "{} {} ({})".format(ins.last_name, ins.first_name, ins.via.name),
                "picture": static('images/default_user_icon.png'),
                "color": "bg-blue" if ins.in_date is not None else "",
                "type": "ext_reg",
                "id": ins.id,
            } for ins in ExternInscription.objects.filter(event=e).select_related('event').select_related('via').order_by('last_name', 'first_name')
        ]
        ret['invits'] = [{
                "display_name": "{} {} (invité par {})".format(ins.first_name, ins.last_name, str(ins.user.profile)),
                "picture": static('images/default_user_icon.png'),
                "color": "bg-blue" if ins.in_date is not None else "",
                "type": "invit",
                "id": ins.id,
            } for ins in Invitation.objects.filter(event=e).select_related('event').select_related('user__profile').order_by('last_name', 'first_name')
        ]
        return JsonResponse(ret)


@permission_required('events.manage_entries')
def management_info_user(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    context = {'type': type, 'iid': iid, 'event': e}
    if type == "reg":
        ins = Inscription.objects.select_related('user__profile').get(event=e, id=iid)
        context['ins'] = ins
        context['display_name'] = str(ins.user.profile)
        context['products'] = [prod for prod in BuyingHistory.get_all_bought_products(ins.user) if prod.event == e]
    elif type == "ext_reg":
        pass
    else:
        pass
    return render(request, "events/admin/info_popup.html", context)


@permission_required('events.manage_entries')
def management_ack(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    if type == "reg":
        ins = Inscription.objects.get(event=e, id=iid)
        ins.in_date = timezone.now()
        ins.save()
        return JsonResponse({"status": 1})
    elif type == "ext_reg":
        pass
    else:
        pass
    return render(request, "events/admin/info_popup.html", context)


@permission_required('events.manage_entries')
def management_nl_ack(request):
    req = json.loads(request.read().decode())
    e = get_object_or_404(Event, id=req['eid'])

    if req['type'] == "reg":
        ins = Inscription.objects.get(event=e, id=req['iid'])
    elif req['type'] == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=req['iid'])
    else:
        ins = Invitation.objects.get(event=e, id=req['iid'])

    ins.payment_mean = req.get("payment_mean")
    ins.in_date = timezone.now()
    ins.save()
    return JsonResponse({"status": 1})


@permission_required('events.manage_entries')
def management_nl_del(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    klass = ""
    if type == "reg":
        ins = Inscription.objects.get(event=e, id=iid)
        if(is_contributor(ins.user)):
            klass = "bg-green"
        else:
            klass = "bg-red"
    elif type == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=iid)
    else:
        ins = Invitation.objects.get(event=e, id=iid)

    ins.payment_mean = None
    ins.in_date = None
    ins.save()
    return JsonResponse({"status": 1, "klass": klass})


@permission_required('events.manage_entries')
def management_nl_info_user(request, eid, type, iid):
    e = get_object_or_404(Event, id=eid)
    context = {'type': type, 'iid': iid, 'eid': eid, 'event': e}
    if type == "reg":
        ins = Inscription.objects.select_related('user__profile').get(event=e, id=iid)
        context['display_name'] = str(ins.user.profile)
    elif type == "ext_reg":
        ins = ExternInscription.objects.get(event=e, id=iid)
        context['display_name'] = "{} {}".format(ins.first_name, ins.last_name)
    else:
        ins = Invitation.objects.get(event=e, id=iid)
        context['display_name'] = "{} {}".format(ins.first_name, ins.last_name)
    context['ins'] = ins
    return render(request, "events/admin/info_nl_popup.html", context)


@permission_required('events.manage_entries')
def management_nl_ack_popup(request, iid, eid):
    context = {"eid": eid, "iid": iid}
    return render(request, "events/admin/nl_ack_popup.html", context)
