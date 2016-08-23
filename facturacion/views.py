from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from gestioneide.models import *
from forms import *

class ReciboListView(ListView):
    model = Recibo
    template_name = "recibos_list.html"

class ReciboCreateView(CreateView):
    model = Recibo
    template_name = "recibo_create.html"
    form_class = ReciboCreateForm
    def get_initial(self):
        year = Year.objects.get(activo=True)
        return { 'year': year }

        
class ReciboDetailView(DetailView):
    model = Recibo
    template_name = "recibo_detail.html"

class ReciboFicheroView(View,SingleObjectMixin):
    model = Recibo
    template_name = "recibo_fichero.html"
    def get(self, request, *args, **kwargs):
        fichero = self.get_object().csb19()
        response = HttpResponse(content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename="csb19.txt"'
        response.write(fichero)
        return response

class ReciboDeleteView(DeleteView):
    model = Recibo
