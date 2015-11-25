import uuid
import hashlib
from core.cache import cache_unless
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.conf import settings
from bde.models import Contributor
from notifications.shortcuts import notify
from . import forms
from . import models


def login(request):
    context = {}

    if request.user.is_authenticated():
        return redirect(request.POST.get('next', reverse('news:index')))
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect(request.POST.get('next', reverse('news:index')))
        else:
            context['error'] = 'Invalid user'

    context['next'] = request.GET.get('next', reverse('news:index'))
    return render(request, 'login.html', context)


@login_required()
def logout(request):
    auth.logout(request)
    return redirect(reverse('news:index'))


@login_required()
def show(request, username):
    try:
        user = User.objects.select_related('profile').get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('news:index'))

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
        elif passwordform.has_changed():
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


def get_contrib(user):
    try:
        return user.contribution.type
    except Contributor.DoesNotExist:
        return None


@login_required
@cache_unless("members", methods=["OPTIONS"])
def members(request):
    if request.method == 'OPTIONS':
        users = [
            {
                'id': user.id,
                'display_name': str(user.profile),
                'picture': user.profile.get_picture_url(),
                'profile_url': user.profile.get_url(),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'nickname': user.profile.nickname,
                'contribution': get_contrib(user),
                'email': user.email,
            } for user in User.objects.select_related('profile').select_related('contribution').all().only('id', 'first_name', 'last_name', 'username', 'profile', 'email', 'contribution',)
        ]
        return JsonResponse({'users': users})

    return render(request, 'accounts/list.html', {})


@login_required
def groups(request):
    if request.method == 'OPTIONS':
        groups = [
            {
                'id': group.id,
                'name': group.name,
                'color': '#%s' % (hashlib.md5(group.name.encode()).hexdigest()[:6]),
            } for group in Group.objects.all()
        ]
        return JsonResponse({'groups': groups})
    return redirect('accounts:list')


def account_request(request):
    if request.user.is_authenticated():
        return redirect(reverse('news:index'))

    if request.method == 'POST':
        form = forms.UserRequestForm(request.POST)
        if form.is_valid():
            form.save()
            notify(
                'Une demande de création de compte à été déposée.',
                'accounts:list_request',
                groups=Group.objects.filter(name=settings.BDE_GROUP_NAME)
            )
            return redirect(reverse('accounts:confirmation'))
    else:
        form = forms.UserRequestForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/request.html', context)


@permission_required('accounts.manage_account_request')
def list_request(request, error=None):
    context = {
        'requests': models.UserRequest.objects.all(),
        'error': error,
    }

    return render(request, 'accounts/list-request.html', context)


ACCEPT_MAIL_TPL="""Bonjour {first_name} {last_name},

Votre compte enib.net à été créé.
Vous pouvez dés maintenant vous connecter avec votre adresse email et le mot de
passe suivant:

{password}

Pour garantir la sécurité de votre compte nous vous conseillons
fortement de le changer dès votre première connexion.
"""


REJECT_MAIL_TPL="""Bonjour {first_name} {last_name},

Votre demande de création de compte sur enib.net à été rejetée.
"""

@permission_required('accounts.manage_account_request')
def accept_request(request, rid):
    user_request = get_object_or_404(models.UserRequest, id=rid)
    username = ("%s_%s" % (user_request.first_name[0], user_request.last_name[:6])).lower()

    if User.objects.filter(email=user_request.email).count() != 0:
        return redirect('accounts:list_request', error='email')
    if User.objects.filter(username=username).count() != 0:
        return redirect('accounts:list_request', error='username')

    with transaction.atomic():
        user = User.objects.create(
            username=username,
            email=user_request.email,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
        )

        password = str(uuid.uuid4())
        user.set_password(password)
        user.save()
        user_request.delete()

        send_mail(
            'Création de votre compte enib.net',
            ACCEPT_MAIL_TPL.format(
                first_name=user_request.first_name,
                last_name=user_request.last_name,
                password=password,
            ),
            'bde@enib.fr',
            [user.email],
            fail_silently=False
        )

    return redirect(reverse('accounts:list_request'))


@permission_required('accounts.manage_account_request')
def reject_request(request, rid):
    user_request = get_object_or_404(models.UserRequest, id=rid)
    user_request.delete()

    send_mail(
        'Rejet de votre demande de création de compte enib.net',
        REJECT_MAIL_TPL.format(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
        ),
        'bde@enib.fr',
        [user_request.email],
        fail_silently=False
    )
    return redirect(reverse('accounts:list_request'))


def confirmation_request(request):
    return render(request, 'accounts/confirmation.html')

