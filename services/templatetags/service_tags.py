from django import template

register = template.Library()


@register.filter(name='upper')
def upper(value):
    return value.upper()


@register.simple_tag
def user_can_mod_service(service, profile):
    return service.can_mod(profile)
