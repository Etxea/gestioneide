from django import template
register = template.Library()
from gestioneide.models import Grupo


#Funcion que recibe un id de grupo y mes y devuelve la respuesta del metodo del objeto que dice que dias hay clase ese mes
@register.filter
def grupo_dias_clase_mes(grupo, mes):
    grupo_obj = Grupo.objects.get(id=grupo)
    dias_clase = grupo_obj.get_dias_clase_mes(mes)
    return dias_clase
