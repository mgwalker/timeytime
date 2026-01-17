from django import template

register = template.Library()


@register.simple_tag
def dump(var):
    return vars(var)
