from django import template
register = template.Library()

@register.filter
def pluck(value, key):
    return [v[key] for v in value]

