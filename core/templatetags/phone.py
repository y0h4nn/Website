from django import template
register = template.Library()


@register.filter
def phone(number):
    return ("{} " * 5).format(*[number[i:i + 2] for i in range(0, len(number), 2)])

