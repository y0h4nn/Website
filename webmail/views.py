from django.shortcuts import render, redirect

WEBMAIL_URLS = {
    'roundcube': 'http://roundcube.enib.net',
    'horde': 'http://imp.enib.net',
    'rainloop': 'http://rainloop.enib.net',
    'squirrel': 'https://imap-eleves.enib.fr',
}

def index(request):
    if request.user.is_authenticated():
        if request.user.webmail_settings.webmail in WEBMAIL_URLS:
            return redirect(WEBMAIL_URLS[request.user.webmail_settings.webmail])

    return render(request, 'webmail/index.html', {})
