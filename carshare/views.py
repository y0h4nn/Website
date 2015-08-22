from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from . import forms
from . import models

def index(request):
    context = {}
    context['announcements'] = models.Announcement.objects.all()
    print(context)
    return render(request, 'carshare/index.html', context)

def show(request, aid):
    announcement = get_object_or_404(models.Announcement, id=aid)

    context = {
        'announcement': announcement,
        'registrations': models.Registration.objects.filter(announcement=announcement).all(),
        'user_is_author': request.user == announcement.author,
    }


    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.announcement = announcement
            registration.user = request.user
            registration.save()
            form.save()
            return redirect(reverse('carshare:show', kwargs={'aid': announcement.id}))
        else:
            context['form'] = form.as_p()
    else:
        context['form'] = forms.RegistrationForm().as_p()

    return render(request, 'carshare/show.html', context)


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

def action(request, aid, rid, state):
    announcement = get_object_or_404(models.Announcement, id=aid)
    registration = get_object_or_404(models.Registration, id=rid)

    if not request.user == announcement.author:
        return redirect(reverse('carshare:show', kwargs={'aid': aid}))

    if state == 'waiting':
        registration.status = None
    elif state == 'accepted' and announcement.available_places() > 0:
        registration.status = 'accepted'
    elif state == 'refused':
        registration.status = 'refused'
    else:
        return redirect(reverse('carshare:show', kwargs={'aid': aid}))

    registration.save()
    return redirect(reverse('carshare:show', kwargs={'aid': aid}))
