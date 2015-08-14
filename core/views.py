from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from webmail.forms import WebmailSettingsForm
from webmail.models import WebmailSettings
from django.contrib.auth.decorators import login_required

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


