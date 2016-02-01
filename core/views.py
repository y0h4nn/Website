from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from webmail.forms import WebmailSettingsForm
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token


def index(request):
    return render(request, 'index.html', {})


@login_required
def settings(request):

    if request.method == "POST":
        error = False
        webmail_settings_form = WebmailSettingsForm(request.POST, instance=request.user.webmail_settings)

        if webmail_settings_form.is_valid():
            webmail_settings_form.save()
        else:
            error = True

        if not error:
            return redirect(reverse('core:settings'))

    else:
        webmail_settings_form = WebmailSettingsForm(instance=request.user.webmail_settings)

    return render(request, 'core/settings.html', {
        'webmail_settings_form': webmail_settings_form.as_p()
    })


@login_required
def api(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = None

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "change":
            if token:
                token.delete()
            token = Token.objects.create(user=request.user)
        elif action == "delete":
            if token:
                token.delete()
        return redirect('core:api')

    return render(request, 'core/api.html', {
        'token': token if token else "Vous n'avez pas de token pour l'api",
    })
