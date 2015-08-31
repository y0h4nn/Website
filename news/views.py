from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from . import forms
from . import models
from bde import bde_member


def index(request):
    context = {
        'news': models.News.objects.order_by('pub_date').all().reverse()[:10],
    }
    return render(request, "news/index.html", context)


@bde_member
def create(request):
    context = {}

    if request.method == "POST":
        form = forms.NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            form.save()
            return redirect(reverse('news:index'))
        else:
            context['form'] = form

    else:
        context['form'] = forms.NewsForm()

    return render(request, "news/create.html", context)

@bde_member
def edit(request, nid):
    n = get_object_or_404(models.News, id=nid)
    if request.method == "POST":
        form = forms.NewsForm(request.POST, instance=n)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:index'))
    else:
        form = forms.NewsForm(instance=n)
    context = {'form': form, 'news': n}
    return render(request, "news/edit.html", context)

