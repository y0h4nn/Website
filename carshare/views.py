from . import forms
from . import models
from datetime import timedelta
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from notifications.shortcuts import notify


@login_required
def index(request):
    context = {}
    context['announcements'] = models.Announcement.objects.filter(date__gt=timezone.now() - timedelta(hours=12))
    return render(request, 'carshare/index.html', context)


@login_required
def show(request, aid):
    announcement = get_object_or_404(models.Announcement.objects.select_related('author__profile'), id=aid)

    context = {
        'announcement': announcement,
        'registrations': models.Registration.objects.filter(announcement=announcement).all().select_related('user__profile'),
        'user_is_author': request.user == announcement.author,
    }


    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.announcement = announcement
            registration.user = request.user
            if request.POST['action'] == 'register' and request.user != announcement.author:
                registration.is_simple_comment = False
                notify(
                    "%s a publié une demande de covoiturage." % str(request.user.profile),
                    "carshare:show", {'aid': aid},
                    [announcement.author],
                )
            else:
                registrations = models.Registration.objects.filter(announcement=announcement).all()
                users = set(reg.user for reg in registrations if reg.user != request.user)
                notify(
                    "%s a commenté une offre de covoiturage à laquelle vous avez participé" % str(request.user.profile),
                    "carshare:show", {'aid': aid},
                    users,
                )
            registration.save()
            form.save()
            return redirect(reverse('carshare:show', kwargs={'aid': announcement.id}))
        else:
            context['form'] = form
    else:
        context['form'] = forms.RegistrationForm()

    return render(request, 'carshare/show.html', context)


@login_required
def create(request):
    context = {}

    if request.method == "POST":
        form = forms.AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            form.save()
            return redirect(reverse('carshare:index'))
        else:
            context['form'] = form.as_p()
    else:
        context['form'] = forms.AnnouncementForm().as_p()
    return render(request, 'carshare/create.html', context)


@login_required
def action(request, aid, rid, state):
    announcement = get_object_or_404(models.Announcement, id=aid)
    registration = get_object_or_404(models.Registration, id=rid)

    if not request.user == announcement.author or registration.status:
        return redirect(reverse('carshare:show', kwargs={'aid': aid}))

    if state == 'accepted' and announcement.available_places() > 0:
        notify(
            "Votre demande de covoiturage a été acceptée",
            "carshare:show", {'aid': announcement.id},
            [registration.user],
        )
        registration.status = 'accepted'
    elif state == 'refused':
        notify(
            "Votre demande de covoiturage a été refusée",
            "carshare:show", {'aid': announcement.id},
            [registration.user],
        )
        registration.status = 'refused'
    else:
        return redirect(reverse('carshare:show', kwargs={'aid': aid}))

    registration.save()
    return redirect(reverse('carshare:show', kwargs={'aid': aid}))



@login_required
def edit(request, aid):
    announcement = get_object_or_404(models.Announcement, id=aid)
    context = {'announcement': announcement}

    if request.user != announcement.author and not request.user.has_perm('carshare.change_announcement'):
        return redirect('news:index')

    if request.method == "POST":
        form = forms.AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            registrations = models.Registration.objects.filter(announcement=announcement).all()
            users = set(reg.user for reg in registrations if reg.user != request.user)
            notify(
                "L'offre de covoiturage a été éditée",
                "carshare:show", {"aid": announcement.id},
                users
            )
            return redirect(reverse('carshare:show', kwargs={'aid': aid}))
        else:
            context['form'] = form
    else:
        context['form'] = forms.AnnouncementForm(instance=announcement)
    return render(request, 'carshare/edit.html', context)


@login_required
def delete(request, aid):
    announcement = get_object_or_404(models.Announcement, id=aid)
    if request.user == announcement.author or request.user.has_perm('carshare.change_announcement'):
        registrations = models.Registration.objects.filter(announcement=announcement).all()
        users = set(reg.user for reg in registrations if reg.user != request.user)
        notify(
            "L'offre de covoiturage a été supprimée",
            "carshare:index", {},
            users
        )
        announcement.delete()
    return redirect(reverse('carshare:index'))


@permission_required('carshare.delete_registration')
def delete_registration(request, rid):
    registration = get_object_or_404(models.Registration, id=rid)
    announcement = registration.announcement
    registration.delete()
    return redirect('carshare:show', aid=announcement.id)
