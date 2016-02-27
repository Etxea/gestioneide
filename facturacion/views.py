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
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReciboListView, self).dispatch(*args, **kwargs)

class ReciboCreateView(CreateView):
    model = Recibo
    template_name = "recibo_create.html"
    form_class = ReciboCreateForm
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReciboCreateView, self).dispatch(*args, **kwargs)  
         
class ReciboDetailView(DetailView):
    model = Recibo
    template_name = "recibo_detail.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReciboDetailView, self).dispatch(*args, **kwargs)  

class ReciboFicheroView(DetailView):
    model = Recibo
    template_name = "recibo_fichero.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReciboFicheroView, self).dispatch(*args, **kwargs)  


class ReciboDeleteView(DeleteView):
    model = Recibo
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReciboDeleteView, self).dispatch(*args, **kwargs)
