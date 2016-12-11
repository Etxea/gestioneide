from django import template
register = template.Library()

@register.filter
def buscar(d, key):
    return d[key]

@register.filter
def mes_texto(mes):
    import calendar
    return calendar.month_name[int(mes)]

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
