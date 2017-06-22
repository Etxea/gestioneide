from django import template
register = template.Library()
from django.utils.translation import ugettext as _
from gestioneide.models import LISTA_MATERIAS_TIPO_EVALUACION

@register.filter
def buscar(d, key):
    return d[key]

@register.filter
def mes_texto(mes):
    import calendar
    return _(calendar.month_name[int(mes)])

@register.filter
def faltas_trimestre(asistencia, trimestre):
    return asistencia.faltas_trimestre(trimestre)

@register.filter
def justificadas_trimestre(asistencia, trimestre):
    return asistencia.justificadas_trimestre(trimestre)

@register.filter
def notas_trimestre(asistencia, trimestre):
    return asistencia.get_nota_trimestre(trimestre)

@register.filter
def notas_cuatrimestre(asistencia, cuatrimestre):
    return asistencia.get_nota_cuatrimestre(cuatrimestre)

@register.filter
def observaciones_trimestre(asistencia, trimestre):
    return asistencia.get_observaciones_trimestre(trimestre)

@register.simple_tag(takes_context=True)
def presente_checked(context,asistencia,mes,dia):
    id_falta = "%s_%s_%s"%(asistencia,mes,dia)
    if id_falta in context['presentes']:
        pos = context['presentes'].index(id_falta)
        presente_id = context['presentes_id'][pos]
        return "name='%s' checked='true'"%presente_id
    else:
        return ""

@register.simple_tag(takes_context=True)
def falta_checked(context,asistencia,mes,dia):
    id_falta = "%s_%s_%s"%(asistencia,mes,dia)
    if id_falta in context['faltas']:
        pos = context['faltas'].index(id_falta)
        falta_id = context['faltas_id'][pos]
        return "name='%s' checked='true'"%falta_id
    else:
        return ""

@register.simple_tag(takes_context=True)
def justificada_checked(context,asistencia,mes,dia):
    id_falta = "%s_%s_%s"%(asistencia,mes,dia)
    if id_falta in context['justificadas']:
        pos = context['justificadas'].index(id_falta)
        justificada_id = context['justificadas_id'][pos]
        return "name='%s' checked='true'"%justificada_id
    else:
        return ""


##Notas
@register.simple_tag(takes_context=True)
def nota_input(context, form, field_name):
    field =form.fields[field_name]
    return field.widget.render(field_name,field.initial)

@register.simple_tag
def nota_display(nota, materia):
    #Primero vemos si en este tipo de curso tiene esa materia o no
    if materia in LISTA_MATERIAS_TIPO_EVALUACION[nota.asistencia.grupo.curso.tipo_evaluacion]:

        #Ahora comprobamos si es no presentado
        np = "%s_np"%str(materia)
        if getattr(nota,np):
            return "NP"
        else:
            return getattr(nota, materia)
    else:
        return "--"