from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from gestioneide.models import *

class YearListView(ListView):
    model=Year
    paginate_by = 50
    template_name = "year/year_list.html"
        
class YearCreateView(CreateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")

class YearUpdateView(UpdateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")


class YearDeleteView(DeleteView):
    template_name = "year/year_deleteconfirm.html"
    def get_success_url(self):
        return reverse_lazy("year_lista")


class YearDetailView(DetailView):
    model = Year
    template_name = "year/year_detail.html"

class YearActivateView(DetailView):
    model = Year
    template_name = "year/year_activate.html"
