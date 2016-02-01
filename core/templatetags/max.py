from django import template
register = template.Library()


@register.filter
def maximum(iterable):
    try:
        return max(iterable)
    except:
        return 0

