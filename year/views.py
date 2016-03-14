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

def year_activate(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        year_actual = Year.objects.get(activo=True)
        year_nuevo = Year.objects.get(id=year_id)
        print "Desactivamos ",year_actual,"activamos",year_nuevo
        year_actual.activo=False
        year_actual.save()
        year_nuevo.activo=True
        year_nuevo.save()
        return HttpResponse(
            { 'msg': "ok"},
            content_type="application/json"
        )


    
