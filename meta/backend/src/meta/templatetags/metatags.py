from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def attr(value, attr_name):
    if hasattr(value, attr_name):
        return getattr(value, attr_name)
    
    if attr_name in value:
        return value[attr_name]

    return ''


@register.filter
def call(value, attr_name, kwargs):
    return getattr(value, attr_name)(**kwargs)