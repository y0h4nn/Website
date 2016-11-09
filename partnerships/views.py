import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.db import models
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddPartnershipForm
from .models import Partnership

@login_required
def index(request):
    partnerships = Partnership.objects.all()
    context = {"partnerships": partnerships}
    return render(request, 'partnerships/index.html',context)


@permission_required('partnerships.manage_partnerships')
def admin_manage_partnerships(request):
    partnerships = Partnership.objects.all()
    context = {"partnerships": partnerships}
    return render(request, 'partnerships/admin/index.html',context)


@permission_required('partnerships.manage_partnerships')
def admin_add_partnership(request):

    if request.method == 'POST':
        form = AddPartnershipForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Le partenariat a été ajouté")
            return redirect(reverse('partnerships:admin_index'))

    else:
        form = AddPartnershipForm()

    return render(request, 'partnerships/admin/add_partnership.html', locals())


@permission_required('partnerships.manage_partnerships')
def admin_delete(request, nid):
    partnership = get_object_or_404(Partnership, id=nid)
    partnership.logo.delete()
    partnership.delete()
    messages.add_message(request, messages.INFO, "Le partenariat a été supprimé")
    return redirect('partnerships:admin_index')


@permission_required('partnerships.manage_partnerships')
def admin_edit(request, nid):
    p = get_object_or_404(Partnership, id=nid)
    oldLogoName = p.logo.name

    if request.method == "POST":
        form = AddPartnershipForm(request.POST, request.FILES, instance = p)

        if form.is_valid():
            from django.conf import settings
            if(os.path.isfile(settings.MEDIA_ROOT+"/"+oldLogoName) and ('logo' in form.changed_data)):
                os.remove(settings.MEDIA_ROOT+"/"+oldLogoName)
            form.save()
            messages.add_message(request, messages.INFO, "Le partenariat a été édité")
            return redirect(reverse('partnerships:admin_index'))
    else:
        form = AddPartnershipForm(instance = p)
    context = {'form': form, 'partnership': p}
    return render(request, "partnerships/admin/edit.html", context)
