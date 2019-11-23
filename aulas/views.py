from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from gestioneide.models import *

@method_decorator(permission_required('gestioneide.aula_view',raise_exception=True),name='dispatch')
class ListaAulas(ListView):
    model = Aula
    template_name="aulas.html"
    context_object_name = "aulas_list"

@method_decorator(permission_required('gestioneide.aula_create',raise_exception=True),name='dispatch')   
class NuevaAula(CreateView):
	model = Aula
	template_name="aula_nueva.html"
	fields="__all__"
	success_url = '/aulas/' ## FIXME esto deberia ser un reverse

@method_decorator(permission_required('gestioneide.aula_change',raise_exception=True),name='dispatch')	
class EditarAula(UpdateView):
	model = Aula
	template_name="aula_editar.html"
	fields = '__all__'
	success_url = "/aulas/"

@method_decorator(permission_required('gestioneide.aula_view',raise_exception=True),name='dispatch')
class DetalleAula(DetailView):
	model = Aula
	context_object_name ="aula"
	template_name="aula_detalle.html"

##FIXME  esto va sin permisos. deberia tener?

def get_clases_dia(fecha,aula=None,profesor=None):
    """funcion que devuelve todas las clases que hay en un dia concreto""" 
    if aula:
        #print "Vamos a listar las de aula %s"%aula
        ret = Clase.objects.filter(hora_inicio__gte=fecha,hora_fin__lte=fecha+datetime.timedelta(days=1),aula=aula)
    elif profesor:
        #print "Vamos a listar las de prfesort %s"%profesor
        ret = Clase.objects.filter(hora_inicio__gte=fecha,hora_fin__lte=fecha+datetime.timedelta(days=1),profesor=profesor)
    else:
        ret = Clase.objects.filter(hora_inicio__gte=fecha,hora_fin__lte=fecha+datetime.timedelta(days=1))
    #print "Encontradas %s clases el dia %s"%(ret.count(),fecha)
    return ret

def programacion_aula_dia(aula,dia):
    #profesor = Profesor.objects.get(id=id)
    clases = []
    for hora in range(8,22):
        ##print "Vamos con la hora %s"%hora
        for cuarto in range(00,60,15):
            fecha_consulta = datetime.datetime(dia.year,dia.month,dia.day,hora,cuarto,0)
            ##print "Vamos con la fecha de consulta %s"%(fecha_consulta)
            clase = Clase.objects.filter(aula=aula, hora_inicio__lte=fecha_consulta,hora_fin__gte=fecha_consulta)
            if clase.count() == 1:
                clase = clase[0]
                ##print "Anadimos la clase es: %s" % clase
                clases.append(["%s:%s"%(hora,cuarto),"%s-%s"%(clase.nombre,clase.aula.nombre)])
            else:
                clases.append(["%s:%s"%(hora,cuarto),"................"])
    return clases
