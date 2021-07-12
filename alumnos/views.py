from django.views.generic import ListView, DetailView
from django.views.generic.edit import View,CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q
from gestioneide.models import *
from alumnos.forms import *


#import logging
#logger = logging.getLogger('gestioneide.debug')
#debug = logger.debug

#Clase base de lista de alumnos

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoListView(ListView):
    model=Alumno
    paginate_by = 75
    template_name = "alumnos/alumno_list.html"
        
@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoActivosListView(AlumnoListView):
    #Solo listamos los activos
    def get_queryset(self):
        return Alumno.objects.filter(activo=True).order_by('id')

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoGrupoListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        ano = Year().get_activo(self.request)
        lista = Asistencia.objects.filter(year=ano)
        return Alumno.objects.filter(asistencia__in=lista).order_by('id')

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoBuscarView(AlumnoListView):
    #Solo listamos los que coinciden conla busqueda
    def get_queryset(self):
        cadena = self.request.GET.get("cadena")
        if cadena.find("@") > 0:
            print("tenemos el email",cadena)
            return Alumno.objects.filter((Q(email__icontains=cadena) | Q(email2__icontains=cadena))).order_by('id')
        try:
            numero = int(cadena)
            # debug("tenemos el numero ",numero)
            if numero > 9999:
                cadena = str(numero)
                return Alumno.objects.filter((Q(telefono1__icontains=cadena) | Q(telefono2__icontains=cadena))).order_by('id')
            else:
                return Alumno.objects.filter(id=numero).order_by('id')
        except:
            # debug("No es un numero, buscamos los que el primer apellido coincida con", cadena)
            palabras = cadena.split(" ")
            if len(palabras)>1:
                filtro = (Q(apellido1__icontains=palabras[0]) & Q(apellido2__icontains=palabras[1])) | (Q(nombre__icontains=palabras[0]) & Q(apellido1__icontains=palabras[1]))
            else:
                filtro = Q(apellido1__icontains=cadena)
            return Alumno.objects.filter(filtro).order_by('id')

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')        
class AlumnoCreateView(CreateView):
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_form.html"
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = "alumnos/alumno_detail.html"

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoDeleteView(DeleteView):
    model = Alumno
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_update_form.html"

    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoBajaView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
    def post(self, request, *args, **kwargs):
        # Look up the author we're interested in.
        self.object = self.get_object()
        #print "Vamos a dar de baja al alumno", self.object
        for asistencia in self.object.asistencia_set.all():
            #print "Borrando asistencia",asistencia
            asistencia.delete()
        hist = Historia(alumno=self.object,tipo="baja",anotacion="")
        hist.save()
        self.object.user.is_active = False
        self.object.user.save()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("alumnos_lista"))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoAnotacionCreateView(CreateView):
    model = Anotacion
    template_name = "alumnos/anotacion_nueva.html"
    fields = ["texto"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoAnotacionCreateView, self).form_valid(form)
    #~ def get_initial(self):
        #~ super(AlumnoAnotacionCreateView, self).get_initial()
        #~ alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        #~ self.initial = {"alumno":alumno.id}
        #~ return self.initial

class AlumnoAnotacionDeleteView(DeleteView):
    model = Anotacion
    template_name = "alumnos/anotacion_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoPruebaNivelCreateView(CreateView):
    model = PruebaNivel
    template_name = "alumnos/pruebanivel_nueva.html"
    fields = ["resultado","nivel_recomendado","observaciones"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoPruebaNivelCreateView, self).form_valid(form)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoPruebaNivelDeleteView(DeleteView):
    model = PruebaNivel
    template_name = "alumnos/confirmar_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoResultadoCambridgeCreateView(CreateView):
    model = ResultadoCambridge
    template_name = "alumnos/resultadocambridge_nuevo.html"
    fields = ["ano","nivel","resultado","observaciones"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoResultadoCambridgeCreateView, self).form_valid(form)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoResultadoCambridgeDeleteView(DeleteView):
    model = ResultadoCambridge
    template_name = "alumnos/confirmar_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

#@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoMailView(CreateView):
    template_name = "alumnos/mail_enviar.html"
    model = MailAlumno
    form_class = EmailAlumnoForm

    def get_context_data(self,**kwargs):
        context = super(AlumnoMailView,self).get_context_data(**kwargs)
        context['alumno'] = Alumno.objects.get(pk=self.kwargs['pk'])
        return context  

    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['pk'])
        form.instance.alumno = alumno
        form.instance.enviado = alumno.enviar_mail(form.cleaned_data['titulo'],form.cleaned_data['mensaje'])
        return super(AlumnoMailView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

class AlumnoMailList(ListView):
    template_name = "alumnos/mail_lista.html"
    model = MailAlumno

    def get_queryset(self):
        alumno = Alumno.objects.get(pk=self.kwargs['pk'])
        return MailAlumno.objects.filter(alumno=alumno)  

    def get_context_data(self,**kwargs):
        context = super(AlumnoMailList,self).get_context_data(**kwargs)
        context['alumno'] = Alumno.objects.get(pk=self.kwargs['pk'])
        return context    


@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoPasswordResetView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        # Look up the author we're interested in.
        self.object = self.get_object()
        self.object.update_user_password()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoCreateUserView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.create_user()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoDisableUserView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user.is_active = False
        self.object.user.save()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoEnableUserView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user.is_active = True
        self.object.user.save()
        return HttpResponseRedirect(reverse_lazy("alumno_detalle",kwargs={'pk': self.object.id}))
