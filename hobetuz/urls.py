# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView,DetailView, ListView, CreateView, UpdateView, DeleteView

from hobetuz.views import *
from hobetuz.forms import *
from hobetuz.models import *


urlpatterns = [
    url(r'^new/2019/$',Registration2019CreateView.as_view(), name="hobetuz_nueva_2019"),
    url(r'^view/2019/(?P<pk>\d+)/$', login_required(Registration2019DetailView.as_view()), name="hobetuz_2019_view"),
    url(r'^list/2019/$',login_required(Registration2019ListView.as_view()), name="hobetuz_list_2019"),
    #url(r'^list/$',RegistrationListView.as_view(), name="hobetuz_list"),
    #url(r'^new/$',RegistrationCreateView.as_view(), name="hobetuz_nueva"),
    #url(r'^excel/$',RegistrationExcelView, name="hobetuz_excel"),
    #url(r'^edit/(?P<pk>\d+)/$',login_required(RegistrationUpdateView.as_view()), name="hobetuz_edit"),
    #url(r'^delete/(?P<pk>\d+)/$',
    #    login_required(DeleteView.as_view(
    #        model=Registration,
    #        success_url="/hobetuz/list/")), name="hobetuz_delete"),
    #url(r'^view/(?P<pk>\d+)/$', ver, name="hobetuz_view"),
    #url(r'^print/(?P<pk>\d+)/$', imprimir_hobetuz, name="hobetuz_imprimir"),
    
    ## Genericas
    url(r'thanks/$', TemplateView.as_view( template_name='hobetuz/gracias.html' ),name="hobetuz_gracias"),
    #~ ##Para los cursos
    #url(r'^curso/list/$',login_required(CursoList.as_view()), name="hobetuz_curso_lista"),
    #url(r'^curso/delete/(?P<pk>\d+)/$',
    #    login_required(DeleteView.as_view(
    #        model=Curso,
    #        success_url="/hobetuz/curso/list/")), name="hobetuz_curso_delete"),
    #url(r'^curso/new/$', login_required(
    #    CreateView.as_view(
    #        model=Curso,
    #        form_class = CursoForm,
    #        success_url = '/hobetuz/curso/list',
    #        template_name='hobetuz/curso_form.html')), name="hobetuz_curso_nuevo"),
    #url(r'^curso/edit/(?P<pk>\d+)/$',
    #    login_required(UpdateView.as_view(
    #        model=Curso,
    #        success_url = '/hobetuz/curso/list',
    #        template_name='hobetuz/curso_edit.html')), name="hobetuz_curso_edit"),
    #url(r'^/?$', HobetuzPortada.as_view(),name="hobetuz"),
]
