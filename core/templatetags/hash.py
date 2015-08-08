from django import template
register = template.Library()

@register.filter
def hash_render(h, key):
    return h[key].widget.render(name=key, value=h[key].initial)

