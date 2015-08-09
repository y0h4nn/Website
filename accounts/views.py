from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from . import forms
from . import models


def login(request):
    context = {}

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect(request.POST.get('next', reverse('core:index')))
        else:
            context['error'] = 'Invalid user'

    context['next'] = request.GET.get('next', reverse('core:index'))
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('core:index'))


@login_required()
def show(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('core:index'))

    context = {
        'user': user,
        'display_name': str(user.profile),
    }
    return render(request, 'accounts/show.html', context)


@login_required()
def edit(request, username):
    if request.user.username != username:
        return redirect(reverse('accounts:show', kwargs={'username': username}))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass

    if request.method == 'POST':
        userform = forms.UserForm(request.POST, instance=user)
        passwordform = auth.forms.PasswordChangeForm(request.user, request.POST)
        profileform = forms.ProfileForm(request.POST, instance=user.profile)
        profileimgform = forms.ImageProfileForm(request.POST, request.FILES, instance=user.profile)
        addressform = forms.AddressForm(request.POST, instance=user.profile.address)

        error = False
        if userform.has_changed() and userform.is_valid():
            userform.save()
        elif userform.has_changed():
            error = True
        else:
            userform = forms.UserForm(instance=user)

        if passwordform.has_changed() and passwordform.is_valid():
            passwordform.save()
        elif passwordform.has_changed() :
            error = True
        else:
            passwordform = auth.forms.PasswordChangeForm(request.user)

        if profileform.has_changed() and profileform.is_valid():
            profileform.save()
        elif profileform.has_changed():
            error = True
        else:
            profileform = forms.ProfileForm(instance=user.profile)

        if profileimgform.has_changed() and profileimgform.is_valid():
            profileimgform.save()
        elif profileimgform.has_changed():
            error = True
        else:
            profileimgform = forms.ImageProfileForm(instance=user.profile)

        if addressform.has_changed() and addressform.is_valid():
            addressform.save()
        elif addressform.has_changed():
            error = True
        else:
            addressform = forms.AddressForm(instance=user.profile.address)


        if error:
            context = {
                'userform': userform.as_p(),
                'passwordform': passwordform.as_p(),
                'profileform': profileform.as_p(),
                'profileimgform': profileimgform.as_p(),
                'addressform': addressform.as_p(),
            }

            return render(request, 'accounts/edit.html', context)
        else:
            return redirect(reverse('accounts:edit', kwargs={'username': username}))

    else:

        userform = forms.UserForm(instance=user)
        passwordform = auth.forms.PasswordChangeForm(request.user)
        profileform = forms.ProfileForm(instance=user.profile)
        profileimgform = forms.ImageProfileForm(instance=user.profile)
        addressform = forms.AddressForm(instance=user.profile.address)

        context = {
            'userform': userform.as_p(),
            'passwordform': passwordform.as_p(),
            'profileform': profileform.as_p(),
            'profileimgform': profileimgform.as_p(),
            'addressform': addressform.as_p(),
        }

        return render(request, 'accounts/edit.html', context)


@login_required()
def members(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'accounts/list.html', context)
