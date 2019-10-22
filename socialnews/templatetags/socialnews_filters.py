from django.template import Library
from django.utils.safestring import mark_safe

import markdown

register = Library()


@register.filter(name='times')
def times(number):
    if number:
        return range(number)


@register.filter(name='markdown')
def markdown_formated(text):
    if text:
        return mark_safe(markdown.markdown(text))
    return ''
