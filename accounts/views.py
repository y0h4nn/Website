from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def login(request):
    context = {}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect(reverse('core:index'))
        else:
            context['error'] = 'Invalid user'

    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('core:index'))
