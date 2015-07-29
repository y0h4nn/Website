from django.core.urlresolvers import reverse
import core.register


def menu(request):
    return {
        'base_menu': core.register.registered_views
    }
