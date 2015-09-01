import json
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from bde import bde_member
from notifications import notify


@login_required
def index(request):
    context = {
        'history': models.BuyingHistory.objects.filter(username=request.user.username).order_by('date').all().reverse()
    }

    return render(request, 'shop/index.html', context)



@bde_member
def sell(request):
    if request.method == 'OPTIONS':
        req = json.loads(request.read().decode())
        try:
            user = User.objects.get(id=req.get('uid'))
        except User.DoesNotExist:
            return JsonResponse({'error': 'L\'utilisateur n\'existe pas.'})

        try:
            product = models.Product.objects.get(id=req.get('pid'))
        except models.Product.DoesNotExists:
            return JsonResponse({'error': 'Le produit selectionné n\'existe pas.'})

        if req.get('payment_mean') not in [p[0] for p in models.MEANS_OF_PAYMENT]:
            return JsonResponse({'error': 'Le moyen de paiement n\'est pas valide'})

        buy = models.BuyingHistory(
            username=user.username,
            product=product.name,
            price=product.price,
            payment_mean=req.get('payment_mean')
        )
        buy.save()
        notify("Confirmation de l'achat de «%s»" % product.name, "shop:index", {}, users=[user])

        if product.action:
            models.ACTIONS_FNC_MAPPING[product.action](user, product, req.get('payment_mean'))

        return JsonResponse({'error': None})
    else:
        context = {
            'products': models.Product.objects.all()
        }
        return render(request, 'shop/sell.html', context)

@bde_member
def history(request):
    context = {
        'history': models.BuyingHistory.objects.order_by('date').all().reverse()
    }

    return render(request, 'shop/history.html', context)


@bde_member
def admin(request):
    if request.method == "POST":
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('shop:admin'))
    else:
        form = forms.ProductForm()

    context = {
        'products': models.Product.objects.all(),
        'form': form.as_p()
    }

    return render(request, 'shop/admin.html', context)


@bde_member
def delete(request, pid):
    product = get_object_or_404(models.Product, id=pid)
    product.delete()
    return redirect(reverse('shop:admin'))
