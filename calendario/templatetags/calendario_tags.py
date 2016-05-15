from django import template
register = template.Library()
from gestioneide.models import *

@register.filter
def festivo(dia):
    #miramos si es fin de semana
    if dia.isoweekday() == 6 or dia.isoweekday() == 7:
        return True
    else:
        return False

@register.filter
def festivo_eide(dia):
    #miramos si esta dado de alta como festivo
    try:
        festivo = Festivo.objects.get(fecha=dia)
        return festivo.id
    except:
        return 0
