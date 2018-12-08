from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView
from django.core.urlresolvers import reverse, reverse_lazy

from models import Mensaje, Comentario

class MensajesListView(ListView):
    model = Mensaje
    context_object_name = "mensajes"
    def get_queryset(self):
        super(MensajesListView, self).get_queryset()
        return Mensaje.objects.filter(creador=self.request.user)

class MensajeCreateView(CreateView):
    model = Mensaje
    fields = "__all__"
    success_url = reverse_lazy('mensajes') 
    def get_initial(self):
        super(CreateView, self).get_initial()
        self.initial = {"creador": self.request.user}
        return self.initial
 

class MensajeDetailView(DetailView):
    model = Mensaje
    context_object_name = "mensaje"

class MensajeRespuestaCreateView(CreateView):
    model = Comentario
    fields = "__all__"
    
    def get_success_url(self):
        print self.object.mensaje
        return reverse('mensaje_ver', kwargs ={'pk': self.object.mensaje.id})

    def get_initial(self):
        super(CreateView, self).get_initial()
        mensaje = Mensaje.objects.get(pk=self.kwargs['mensaje_id'])
        self.initial = {"mensaje":mensaje.id, "creador": self.request.user}
        return self.initial
 
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['mensaje_obj'] = Mensaje.objects.get(pk=self.kwargs['mensaje_id'])
        return context