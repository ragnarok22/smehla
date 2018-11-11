from django import template

register = template.Library()


@register.filter(name='upper')
def upper(value):
    return value.upper()


@register.simple_tag
def my_tag(service, profile):
    return service.can_mod(profile)
