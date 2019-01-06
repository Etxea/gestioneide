from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

from models import Mensaje, Comentario
from forms import *

class MensajesListView(ListView):
    model = Mensaje
    context_object_name = "mensajes"
    def get_queryset(self):
        super(MensajesListView, self).get_queryset()
        return Mensaje.objects.filter(creador=self.request.user).exclude(todos=True)

class MensajeCreateView(CreateView):
    model = Mensaje
    fields = "__all__"
    success_url = reverse_lazy('mensajes') 
    def get_initial(self):
        super(CreateView, self).get_initial()
        self.initial = {"creador": self.request.user}
        return self.initial

class MensajeAllView(View):
    form_class = MensajeAllForm
    initial = {'key': 'value'}
    template_name = 'mensajes/mensaje_all_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            for user in User.objects.all():
                men = Mensaje(creador=self.request.user,destinatario=user,todos=True,\
                titulo=form.cleaned_data['titulo'],\
                texto=form.cleaned_data['mensaje'])
                men.save()
            return HttpResponseRedirect('/mensajes/')

        return render(request, self.template_name, {'form': form})


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