from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from gestioneide.models import *

class AsistenciaListView(ListView):
    model=Asistencia
    paginate_by = 50
    template_name = "asistencia/asistencia_list.html"
        
class AsistenciaCreateView(CreateView):
    template_name = "asistencia/asistencia_form.html"
    model = Asistencia
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")

class AsistenciaUpdateView(UpdateView):
    template_name = "asistencia/asistencia_form.html"
    model = Asistencia
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")


class AsistenciaDeleteView(DeleteView):
    template_name = "asistencia/asistencia_deleteconfirm.html"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")


class AsistenciaDetailView(DetailView):
    model = Asistencia
    template_name = "asistencia/asistencia_detail.html"
