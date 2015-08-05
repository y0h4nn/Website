from django import template
from django.core.urlresolvers import reverse, resolve

register = template.Library()

@register.inclusion_tag('core/tags/menu_item.html', takes_context=True)
def _base_menu_item(context, name, view, *args, **kwargs):
    request = context['request']
    selected = False
    try:
        namespace, _ = view.split(':')
    except ValueError:
        namespace = None

    if namespace in resolve(request.path).namespaces:
        selected = True

    return {
        'name': name,
        'url': reverse(view, args=args, kwargs=kwargs),
        'selected': 'selected' if selected else ''
    }

@register.inclusion_tag('core/tags/menu_item.html', takes_context=True)
def menu_item(context, name, view, *args, **kwargs):
    request = context['request']
    selected = False

    if view == resolve(request.path).view_name:
        selected = True

    return {
        'name': name,
        'url': reverse(view, args=args, kwargs=kwargs),
        'selected': 'selected' if selected else ''
    }

