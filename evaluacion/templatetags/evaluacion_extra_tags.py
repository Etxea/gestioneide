from django import template
register = template.Library()

@register.filter
def buscar(d, key):
    return d[key]
