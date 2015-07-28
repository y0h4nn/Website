from django.core.urlresolvers import reverse


def menu(request):
    menu = [
        {'name': 'Accueil', 'url': reverse('core:index')}
    ]

    if request.user.is_active:
        menu.append(
            {
                'name': 'Profil',
                'url': reverse('accounts:show', kwargs={'username': request.user.username}),
            }
        )
    return {
        'base_menu': menu
    }
