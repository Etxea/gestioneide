# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView,DetailView, ListView, CreateView, UpdateView, DeleteView

from views import *
from forms import *
from models import *


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
