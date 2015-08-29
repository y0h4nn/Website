from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
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
            context['form'] = form.as_p()

    else:
        context['form'] = forms.NewsForm().as_p()

    return render(request, "news/create.html", context)
