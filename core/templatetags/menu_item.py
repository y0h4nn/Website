from django import template
from django.core.urlresolvers import reverse, resolve

register = template.Library()

@register.inclusion_tag('core/tags/menu_item.html', takes_context=True)
def menu_item(context, name, view, *args, **kwargs):
    request = context['request']
    selected = False

    if resolve(request.path).view_name == view:
        selected = True

    return {
        'name': name,
        'url': reverse(view, args=args, kwargs=kwargs),
        'selected': 'selected' if selected else ''
    }
