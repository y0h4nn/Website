from .forms import PizzaAddingForm, PizzaTakingForm, CommandForm
from .models import Pizza, Inscription, Command
from collections import Counter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from bde.shortcuts import bde_member
import csv
import json


@login_required
def index(request):
    pizzas = Pizza.objects.filter(deleted=False)
    com = Command.get_current()
    if com is None or not com.is_valid():
        return render(request, 'pizza/no_command.html')
    if request.method == "OPTIONS":
        req = json.loads(request.read().decode())
        ins = Inscription.objects.get(user=request.user, id=req['iid'])
        ins.delete()
        return JsonResponse({"status": 1})
    elif request.method == "POST":
        form = PizzaTakingForm(request.POST, pizzas=pizzas)
        if form.is_valid():
            chosen = Pizza.objects.get(id=form.cleaned_data['pizza'])
            ins = Inscription(user=request.user, pizza=chosen, command=com)
            ins.save()
            messages.add_message(request, messages.INFO, "Votre commande a bien été prise en compte")
            return redirect('pizza:index')

    ins = Inscription.objects.filter(user=request.user, command=com).select_related("pizza")
    form = PizzaTakingForm(pizzas=pizzas)
    context = {"pizzas": pizzas, 'form': form, 'command': com, 'inscriptions': ins}
    return render(request, 'pizza/index.html', context)


@bde_member
def admin_index(request):
    command_list = Command.objects.all().prefetch_related('inscriptions__pizza').prefetch_related('inscriptions__user__profile').order_by("inscriptions__user")
    paginator = Paginator(command_list, 1)

    page = request.GET.get('page')
    try:
        commands = paginator.page(page)
    except PageNotAnInteger:
        commands = paginator.page(1)
    except EmptyPage:
        commands = paginator.page(paginator.num_pages)

    # As we have only one command by page this is always true.
    try:
        command = commands[0]
    except IndexError:
        return render(request, 'pizza/admin/no_command.html')
    pizzas = Counter([ins.pizza for ins in command.inscriptions.all().select_related('pizza')])

    return render(request, 'pizza/admin/index.html', {'commands': commands, 'pizzas': dict(pizzas.items())})


@bde_member
def admin_manage_pizzas(request):
    if request.method == 'POST':
        form = PizzaAddingForm(request.POST)
        if form.is_valid():
            form.save()
    elif request.method == 'OPTIONS':
        req = json.loads(request.read().decode())
        p = Pizza.objects.get(id=req['pid'])
        p.deleted = True
        p.save()
        return JsonResponse({'status': 1})
    else:
        form = PizzaAddingForm()
    pizzas = Pizza.objects.filter(deleted=False)
    context = {'form': form, 'pizzas': pizzas}
    return render(request, 'pizza/admin/manage_pizzas.html', context)


@bde_member
def admin_manage_commands(request):
    com = Command.get_current()
    if com is not None and com.is_valid():
        form = CommandForm(request.POST or None, initial=com.__dict__)
    else:
        form = CommandForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "La commande a été sauvegardée")

    return render(request, 'pizza/admin/manage_commands.html', {'form': form})

@bde_member
def admin_export_csv(request, cid):
    command = get_object_or_404(Command, id=cid)
    reg = Inscription.objects.filter(command=command).select_related("user__profile").order_by('user')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pizzas_{}.csv"'.format(command.date)

    writer = csv.writer(response)
    writer.writerow(['Login', 'Surnom', 'Prénom', 'Nom', 'Mail', 'From', 'Pizza'])
    for r in reg:
        line = [r.user.profile.user, r.user.profile.nickname, r.user.first_name, r.user.last_name, r.user.email, "ENIB", r.pizza.name]
        writer.writerow(line)
    return response

