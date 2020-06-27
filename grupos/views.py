from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from grupos.forms import *
from gestioneide.models import *
import calendar

@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoListView(ListView):
    model=Grupo
    paginate_by = 100
    template_name = "grupos/grupo_list.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoListView, self).get_context_data(**kwargs)
        context['centros_list'] = Centro.objects.all()
        try:
            centro = Centro.objects.get(id=self.kwargs['centro'])
            context['centro_seleccionado'] = centro
        except:
            pass
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        #Si es staff ve todos los grupos
        try:
            centro = Centro.objects.get(id=self.kwargs['centro'])
        except:
            centro = None

        if self.request.user.is_staff:
            if centro:
                return Grupo.objects.filter(year=year).filter(centro=centro).order_by('nombre')
            else:
                return Grupo.objects.filter(year=year).order_by('nombre')
        #Sino limitamos los grupos a los cuales el profesor da clase
        else:
            if centro:
                return Grupo.objects.filter(centro=centro).filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))
            else:
                return Grupo.objects.filter(
                    clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))

#@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoProfesorListView(ListView):
    model=Grupo
    paginate_by = 100
    template_name = "grupos/grupo_profesor_list.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoProfesorListView, self).get_context_data(**kwargs)
        context['centros_list'] = Centro.objects.all()
        try:
            centro = Centro.objects.get(id=self.kwargs['centro'])
            context['centro_seleccionado'] = centro
        except:
            pass
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        #Si es staff ve todos los grupos
        try:
            centro = Centro.objects.get(id=self.kwargs['centro'])
        except:
            centro = None

        if self.request.user.is_staff:
            if centro:
                return Grupo.objects.filter(year=year).filter(centro=centro).order_by('nombre')
            else:
                return Grupo.objects.filter(year=year).order_by('nombre')
        #Sino limitamos los grupos a los cuales el profesor da clase
        else:
            if centro:
                return Grupo.objects.filter(centro=centro).filter(year=year).filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))
            else:
                return Grupo.objects.filter(year=year).filter(
                    clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))

@method_decorator(permission_required('gestioneide.grupo_add',raise_exception=True),name='dispatch')        
class GrupoCreateView(CreateView):
    form_class = GrupoCreateForm
    template_name = "grupos/grupo_form.html"
    def get_success_url(self):
        return reverse_lazy("grupo_lista")

@method_decorator(permission_required('gestioneide.view_data_grupo',raise_exception=True),name='dispatch')
class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_detail.html"

## FIXME lo idea seria hacer un control mas fino, solo pueden ver detalles los profesores que tienen clase en el grupo
@method_decorator(permission_required('gestioneide.view_data_grupo',raise_exception=True),name='dispatch')
class GrupoProfesorDetailView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_detail.html"

@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoEmailView(FormView):
    template_name = 'grupos/email_form.html'
    form_class = ContactForm
    
    def get_context_data(self, **kwargs):
        context = super(GrupoEmailView, self).get_context_data(**kwargs)
        context['grupo_id'] = self.kwargs['pk']
        return context
    
    def get_initial(self):
        #grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        #print("Somo get initial y tenemos: %s"%self.kwargs['pk'])
        return { 'group_id': self.kwargs['pk'] , 'user_id': self.request.user.id }
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(GrupoEmailView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.kwargs['pk']})

@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoEmailHorarioView(FormView):
    template_name = 'grupos/grupo_email_horarios_form.html'
    form_class = GrupoHorarioEmailForm
    
    def get_context_data(self, **kwargs):
        context = super(GrupoEmailHorarioView, self).get_context_data(**kwargs)
        context['grupo_id'] = self.kwargs['pk']
        return context
    
    def get_initial(self):
        return { 'group_id': self.kwargs['pk'] , 'user_id': self.request.user.id }
    
    def form_valid(self, form):
        form.send_email()
        return super(GrupoEmailHorarioView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.kwargs['pk']})

@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoEmailHorarioHtmlView(DetailView):
    template_name = "grupos/email_horario.html"
    model = Grupo
    context_object_name = 'grupo'

    def get_context_data(self, **kwargs):
        context = super(GrupoEmailHorarioHtmlView, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['lista_festivos'] =Festivo.objects.filter(year=year)
        return context

@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoAlumnoEmailView(FormView):
    template_name = 'grupos/email_alumno_form.html'
    form_class = ContactAlumnoForm

    def get_initial(self):
        #grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        #print("Somo get initial y tenemos: %s"%self.kwargs['pk'])
        return { 'asistencia_id': self.kwargs['pk'] , 'user_id': self.request.user.id }

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(GrupoAlumnoEmailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(GrupoAlumnoEmailView, self).get_context_data(**kwargs)
        context['asistencia_id'] = self.kwargs['pk']
        return context
    
    def get_success_url(self):
        asistencia = Asistencia.objects.get(id=self.kwargs['pk'])
        return reverse_lazy("grupo_detalle", kwargs={'pk': asistencia.grupo.id })
    
@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoAsistenciaView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_planilla_asistencias.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoAsistenciaView, self).get_context_data(**kwargs)
        cal = calendar.Calendar()
        mes = int(self.kwargs['mes'])
        mes_nombre = calendar.month_name[mes]
        context['mes'] = mes
        context['mes_nombre'] = mes_nombre      
        return context

@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoNotasView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_planilla_notas.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoNotasView, self).get_context_data(**kwargs)
        context['trimestre'] = self.kwargs['trimestre']
        conceptos = ['Grammar','lalala','lelele']
        context['conceptos'] = conceptos
        return context

@method_decorator(permission_required('gestioneide.grupo_delete',raise_exception=True),name='dispatch')
class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = "grupos/grupo_confirm_delete.html"    
    def get_success_url(self):
        return reverse_lazy("grupo_lista")

@method_decorator(permission_required('gestioneide.grupo_change',raise_exception=True),name='dispatch')
class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoCreateForm
    template_name = "grupos/object_update_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")

class GrupoAnotacionCreateView(CreateView):
    model = AnotacionGrupo
    template_name = "grupos/anotacion_nueva.html"
    fields = ["texto"]

    def get_success_url(self):
        return reverse_lazy("grupo_profesor_detalle", kwargs={'pk': self.object.grupo.pk})
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        grupo = Grupo.objects.get(pk=self.kwargs['grupo_id'])
        form.instance.grupo = grupo
        return super(GrupoAnotacionCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(GrupoAnotacionCreateView, self).get_context_data(**kwargs)
        context['grupo_id'] = self.kwargs['grupo_id']
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        form = super(GrupoAnotacionCreateView, self).get_form(form_class)
        form.fields['texto'].widget = forms.Textarea()
        return form
    
    def get_initial(self):
        #grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        #print("Somo get initial y tenemos: %s"%self.kwargs['pk'])
        return { 'group_id': self.kwargs['grupo_id'] , 'creador_id': self.request.user.id }        

class GrupoAnotacionDetailView(DetailView):
    model = AnotacionGrupo
    template_name = "grupos/anotaciongrupo_detail.html"

class GrupoAnotacionModalView(DetailView):
    model = AnotacionGrupo
    template_name = "grupos/anotacion_modal_view.html"

class GrupoAnotacionDeleteView(DeleteView):
    model = AnotacionGrupo
    template_name = "grupo/anotacion_borrar.html"
    def get_success_url(self):
        return reverse_lazy("grupo_profesor_detalle",kwargs={'pk': self.object.grupo.pk})

##FIXME anadir control para que solo staff o profesor pueda editar su clase y no todos todas
class GrupoClaseVideurlCreateView(UpdateView):
    model = Clase
    template_name = "grupos/videourl_update.html"
    fields = ["video_url"]

    def get_success_url(self):
        return reverse_lazy("grupo_profesor_detalle", kwargs={'pk': self.object.grupo.pk})
    
    # def form_valid(self, form):
    #     form.instance.creador = self.request.user
    #     grupo = Grupo.objects.get(pk=self.kwargs['grupo_id'])
    #     form.instance.grupo = grupo
    #     return super(GrupoAnotacionCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(GrupoClaseVideurlCreateView, self).get_context_data(**kwargs)
        context['grupo_id'] = self.kwargs['grupo_id']
        return context

    # def get_form(self, form_class=None):
    #     if form_class is None:
    #         form_class = self.form_class
    #     form = super(GrupoAnotacionCreateView, self).get_form(form_class)
    #     form.fields['texto'].widget = forms.Textarea()
    #     return form
    
    # def get_initial(self):
    #     #grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
    #     #print("Somo get initial y tenemos: %s"%self.kwargs['pk'])
    #     return { 'group_id': self.kwargs['grupo_id'] , 'creador_id': self.request.user.id }        

@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoNotasTrimestreEmailView(View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        print("Vamos a enviar las notas del grupo %s del trimestre %s"%(kwargs['pk'],kwargs['trimestre']))
        try:
            grupo = Grupo.objects.get(pk=kwargs['pk'])
            grupo.envio_notas_email('trimestre',kwargs['trimestre'])
        except Exception as e:
            print("Error",e)
            mensaje = "Error"
        return redirect(grupo)
    
@method_decorator(permission_required('gestioneide.send_email_grupo',raise_exception=True),name='dispatch')
class GrupoNotasCuatrimestreEmailView(View):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        print("Vamos a enviar las notas del grupo %s del cuatrimestre %s"%(kwargs['pk'],kwargs['cuatrimestre']))
        try:
            grupo = Grupo.objects.get(pk=kwargs['pk'])
            grupo.envio_notas_email('cuatrimestre',kwargs['cuatrimestre'])
        except Exception as e:
            print("Error",e)
            mensaje = "Error"
        return redirect(grupo)

    