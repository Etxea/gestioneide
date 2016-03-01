from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
        
class ReciboDetailView(DetailView):
    model = Recibo
    template_name = "recibo_detail.html"

class ReciboFicheroView(DetailView):
    model = Recibo
    template_name = "recibo_fichero.html"

class ReciboDeleteView(DeleteView):
    model = Recibo
