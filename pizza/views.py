from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Pizza, Inscription, Command
from .forms import PizzaAddingForm, PizzaTakingForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import Counter


def index(request):
    pizzas = Pizza.objects.filter(deleted=False)
    com = Command.get_current()

    try:
        ins = Inscription.objects.get(user=request.user, command=com)
        return render(request, 'pizza/already.html', {'command': com})
    except Inscription.DoesNotExist:
        pass

    if request.method == "POST":
        form = PizzaTakingForm(request.POST, pizzas=pizzas)
        if form.is_valid():
            chosen = Pizza.objects.get(id=form.cleaned_data['pizza'])
            command = Command.get_current()
            ins = Inscription(user=request.user, pizza=chosen, command=com)
            ins.save()
            messages.add_message(request, messages.INFO, "Votre commande a bien été prise en compte")
            return redirect('news:index')

    form = PizzaTakingForm(pizzas=pizzas)
    context = {"pizzas": pizzas, 'form': form, 'command': com}
    return render(request, 'pizza/index.html', context)


def admin_index(request):
    command_list = Command.objects.all().prefetch_related('inscriptions__pizza').prefetch_related('inscriptions__user__profile')
    paginator = Paginator(command_list, 1)

    page = request.GET.get('page')
    try:
        commands = paginator.page(page)
    except PageNotAnInteger:
        commands = paginator.page(1)
    except EmptyPage:
        commands = paginator.page(paginator.num_pages)

    # As we have only one command by page this is always true.
    command = commands[0]
    pizzas = Counter([ins.pizza for ins in command.inscriptions.all().select_related('pizza')])

    return render(request, 'pizza/admin/index.html', {'commands': commands, 'pizzas': dict(pizzas.items())})


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
