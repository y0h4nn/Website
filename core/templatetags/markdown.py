import markdown as _markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def markdown(value):
    md = _markdown.markdown(value)
    return mark_safe('<div class="markdown">%s</div>' % md)
