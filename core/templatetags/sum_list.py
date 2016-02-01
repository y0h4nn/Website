from django import template
register = template.Library()


@register.filter
def sum_list(l):
    return sum(l)

