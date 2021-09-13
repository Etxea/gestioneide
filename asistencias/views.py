from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect
from gestioneide.models import *
from asistencias.forms import *

@method_decorator(permission_required('gestioneide.asistencia_view',raise_exception=True),name='dispatch')
class AsistenciaDeletedListView(ListView):
    model=Asistencia
    paginate_by = 50
    template_name = "asistencias/asistencia_deleted_list.html"
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.all_objects.filter(borrada=True).filter(year=year)

@method_decorator(permission_required('gestioneide.asistencia_view',raise_exception=True),name='dispatch')
class AsistenciaListView(ListView):
    model=Asistencia
    paginate_by = 50
    template_name = "asistencias/asistencia_list.html"
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.objects.filter(year=year)

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')        
class AsistenciaCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","alumno","confirmado","factura","metalico","precio"]
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("asistencia_lista")

    def get_initial(self):
        year = Year().get_activo(self.request)
        #print "Establecemos el ano en ",year
        return { 'year': year }

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')        
class AsistenciaAlumnoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","confirmado","factura","metalico","precio"]
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super(AsistenciaAlumnoCreateView, self).get_form(form_class)
        form.fields['grupo'].queryset = Grupo.objects.filter(year=Year().get_activo(self.request))
        return form

    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs = {'pk' : self.object.alumno.pk })

    def get_initial(self):
        year = Year().get_activo(self.request)
        alumno = Alumno.objects.get(id=self.kwargs['alumno_id'])
        #print "Establecemos el ano en ",year,"y el alumno en",alumno
        return { 'year': year , 'alumno': alumno }        

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')
class AsistenciaGrupoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    form_class = AsistenciaGrupoCreateForm
    #fields = ["alumno","confirmado","factura","metalico","precio"]

    def get_success_url(self):
        return reverse_lazy("grupo_detalle",kwargs = {'pk' : self.object.grupo.id })
        
    def get_initial(self):
        year = Year().get_activo(self.request)
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        print("Establecemos el ano en ",year, "y el grupo",grupo)
        return { 'year': year , 'grupo': grupo }        

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.save()
    #     self.object.year = Year().get_activo(self.request)
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())
    
@method_decorator(permission_required('gestioneide.asistencia_change',raise_exception=True),name='dispatch')
class AsistenciaUpdateView(UpdateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    fields = "__all__"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        form = super(AsistenciaUpdateView, self).get_form(form_class)
        form.fields['grupo'].queryset = Grupo.objects.filter(year=self.object.year)
        return form

    def get_success_url(self):
        return reverse_lazy("alumno_detalle",args=[self.object.alumno.id])

@method_decorator(permission_required('gestioneide.asistencia_delete',raise_exception=True),name='dispatch')
class AsistenciaDeleteView(DeleteView):
    template_name = "asistencias/asistencia_deleteconfirm.html"
    model = Asistencia
    ##FIXME esto deberia ser dinamico
    def get_success_url(self):
        return reverse_lazy("grupo_detalle",kwargs = {'pk' : self.object.grupo.id })

@method_decorator(permission_required('gestioneide.asistencia_view',raise_exception=True),name='dispatch')
class AsistenciaDetailView(DetailView):
    model = Asistencia
    template_name = "asistencias/asistencia_detail.html"

@permission_required('gestioneide.year_add',raise_exception=True)
def asistencia_domiciliacion(request):
    if request.method == 'POST':
        asistencia_id = request.POST.get('id')
        asistencia = Asistencia.objects.get(id=asistencia_id)
        
        asistencia.metalico=False
        asistencia.save()
        
        return JsonResponse({'state':'ok','msg': "done"})
    else:
        return HttpResponseRedirect(reverse('asistencia_lista'))

@permission_required('gestioneide.year_add',raise_exception=True)
def asistencia_recuperar(request):
    if request.method == 'POST':
        asistencia_id = request.POST.get('id')
        asistencia = Asistencia.all_objects.get(id=asistencia_id)
        year = Year().get_activo(request)
        asistencia.borrada=False
        hist = Historia(
			alumno=asistencia.alumno, tipo="recuperar", 
			anotacion="Recuperara la asistencia del grupo %s ano %s"%(asistencia.grupo.nombre, year))
        hist.save()
        asistencia.save()        
        return JsonResponse({'state':'ok','msg': "done"})
    else:
        return HttpResponseRedirect(reverse('asistencia_deleted_lista'))


class EnvioNotaTrimestre(View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        print("Vamos a enviar las notas de la asistencia %s del trimestre %s"%(kwargs['pk'],kwargs['trimestre']))
        try:
            asistencia = Asistencia.objects.get(pk=kwargs['pk'])
            asistencia.envio_notas_email('trimestre',kwargs['trimestre'])
        except Exception as e:
            print("Error",e)
            mensaje = "Error"
        return redirect(grupo)

class EnvioHorario(View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        print("Vamos a enviar el horario de la asistencia %s")
        try:
            asistencia = Asistencia.objects.get(pk=kwargs['pk'])
            #asistencia.envio_horario()
            context={}
            context['grupo'] = self.grupo
            year = grupo.year
            context['lista_festivos'] =Festivo.objects.filter(year=year) 
            #context['message'] = self.cleaned_data["message"]
            titulo = "Horarios %s"%grupo.year
            mensaje = render_to_string('grupos/email_horario.html', context=context)
            alumno = asistencia.alumno    
            mail = MailAlumno()
            mail.alumno = alumno
            mail.creador = self.request.user
            mail.titulo = titulo
            mail.mensaje = mensaje[:490]
            try:
                from_email=mail.creador.profesor.email
            except:
                from_email=None
            mail.enviado = alumno.enviar_mail(titulo,mensaje,from_email=from_email,mensaje_html=True)
            mail.save()
        except Exception as e:
            print("Error",e)
            mensaje = "Error"
        return redirect(asistencia.grupo)        
