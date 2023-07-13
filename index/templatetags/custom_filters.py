from cgi import print_form
from django import template

register = template.Library()


@register.simple_tag
def replace(value, old, new):
    return value.replace(old, new)
