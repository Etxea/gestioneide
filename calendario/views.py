from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from calendario.forms import *
from gestioneide.models import *
import calendar

@method_decorator(permission_required('gestioneide.festivo_delete',raise_exception=True),name='dispatch')
class BorrarFestivo(DeleteView):
    model = Festivo
    template_name = "calendario/festivo_confirm_delete.html"
    success_url = "/calendario"

@method_decorator(permission_required('gestioneide.festivo_view',raise_exception=True),name='dispatch')
class ListaFestivos(ListView):
    model = Festivo
    paginate_by = 25
    template_name = "calendario/festivos_lista.html"

@method_decorator(permission_required('gestioneide.festivo_view',raise_exception=True),name='dispatch')
class CalendarioFestivos(ListView):
    model = Festivo
    template_name = "calendario/festivos_calendario.html"
    
    def get_context_data(self, **kwargs):
        context = super(CalendarioFestivos, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        meses = []
        cal = calendar.Calendar()
        lista_meses_1 = [9,10,11,12]
        lista_meses_2 = [1,2,3,4,5,6,7]
        for mes in lista_meses_1:
            meses.append({"numero": mes, "nombre": calendar.month_name[mes],"calendario": cal.monthdatescalendar(year.start_year,mes)})
        for mes in lista_meses_2:
            meses.append({"numero": mes,"nombre": calendar.month_name[mes],"calendario": cal.monthdatescalendar(year.start_year+1,mes)})
        context['meses'] = meses
        return context

@method_decorator(permission_required('gestioneide.festivo_change',raise_exception=True),name='dispatch')
class EditarFestivo(UpdateView):
    model = Festivo
    template_name = "calendario/festivo_editar.html"
    fields = "__all__"
    success_url = "/calendario"

@method_decorator(permission_required('gestioneide.festivo_add',raise_exception=True),name='dispatch')
class NuevoFestivo(CreateView):
    model = Festivo
    success_url = "/calendario"
    fields = "__all__"
    template_name = "calendario/festivo_nuevo.html"
    def get_initial(self):
        if self.kwargs.get('ano'):
            fecha = self.kwargs.get('ano')+"-"+self.kwargs.get('mes')+"-"+self.kwargs.get('dia')
            year = Year().get_activo(self.request)
            return {
                'fecha':fecha,
                'year': year
            }

@method_decorator(permission_required('gestioneide.festivo_view',raise_exception=True),name='dispatch')  
class DetalleFestivo(DetailView):
    model = Festivo
    template_name = "festivo_detalle.html"
