from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from gestioneide.models import *
from forms import *



class ProfesorCreateView(CreateView):
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfesorCreateView, self).dispatch(*args, **kwargs)


class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = "profesores/profesor_detail.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfesorDetailView, self).dispatch(*args, **kwargs)

class ProfesorDeleteView(DeleteView):
    model = Profesor
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfesorDeleteView, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("profesores_lista")

class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_update_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfesorUpdateView, self).dispatch(*args, **kwargs)
        
def get_profesores_libres(hora_incio,hora_fin):
    pass
    
def programacion_profesor_dia(profesor,dia):
    #profesor = Profesor.objects.get(id=id)
    clases = []
    for hora in range(8,22):
        #print "Vamos con la hora %s"%hora
        for cuarto in range(00,60,15):
            fecha_consulta = datetime.datetime(dia.year,dia.month,dia.day,hora,cuarto,0)
            #print "Vamos con la fecha de consulta %s"%(fecha_consulta)
            clase = Clase.objects.filter(profesor=profesor, hora_inicio__lte=fecha_consulta,hora_fin__gte=fecha_consulta)
            if clase.count() == 1:
                clase = clase[0]
                #print "Anadimos la clase es: %s" % clase
                clases.append(["%s:%s"%(hora,cuarto),"%s-%s"%(clase.nombre,clase.aula.nombre)])
            else:
                clases.append(["%s:%s"%(hora,cuarto),""])
    return clases
        
