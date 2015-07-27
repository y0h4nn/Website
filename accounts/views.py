from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from . import forms

def login(request):
    context = {}

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect(reverse('core:index'))
        else:
            context['error'] = 'Invalid user'

    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('core:index'))

# TODO require login
def show(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('core:index'))

    context = {
        'last_name': user.last_name or "Donnée inconue",
        'first_name': user.first_name or "Donnée inconue",
        'email': user.email,
        'groups': ', '.join(user.groups.all()) or "L'utilisateur n'est pas membre d'un groupe",
        'perms': ', '.join(user.user_permissions.all()) or "L'utilisateur n'a aucune permissions",
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }
    return render(request, 'accounts/show.html', context)

def edit(request, username):
    if request.user.username != username:
        return redirect(reverse('accounts:show', kwargs={'username': username}))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass

    if request.method == 'POST':
        userform = forms.UserForm(request.POST, instance=user)
        profileform = forms.ProfileForm(request.POST, instance=user.profile)

        error = False
        if userform.has_changed() and userform.has_changed():
            userform.save()
        elif not userform.is_valid():
            error = True
            print("bad user form")

        if profileform.has_changed() and profileform.is_valid():
            profileform.save()
        elif not profileform.is_valid():
            error = True
            print("bad profile form")

        if error:
            return redirect(reverse('accounts:edit', kwargs={'username': username}))
        else:
            return redirect(reverse('accounts:show', kwargs={'username': username}))

    else:
        userform = forms.UserForm(instance=user)
        profileform = forms.ProfileForm(instance=user.profile)

        context = {
            'userform': userform.as_p(),
            'profileform': profileform.as_p(),
        }

        return render(request, 'accounts/edit.html', context)
