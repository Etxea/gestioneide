from django import template

register = template.Library()

def calcular_precio(precio, medio):
    """Removes all values of arg from the given string"""
    if medio:
	    return precio/2
    else:
        return precio


register.filter('calcular_precio', calcular_precio)

