import markdown as _markdown
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape, strip_tags

register = template.Library()

@register.filter
def markdown(value):
    md = _markdown.markdown(escape(strip_tags(value)))
    return mark_safe('<div class="markdown">%s</div>' % md)
