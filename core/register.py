from django.core.urlresolvers import reverse_lazy

registered_views = []

def menu_item(name, target, **kwargs):
    registered_views.append({
        'name': name,
        'url': reverse_lazy(target, kwargs=kwargs)
    })

