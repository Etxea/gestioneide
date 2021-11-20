# -*- coding: utf-8 -*-
from django.conf.urls import url
from matriculas.views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'pagar/(?P<type>\w+)/(?P<pk>\d+)/$',MatriculaPayView.as_view(), name="matricula_pagar"),
    ## LINGUASKILSS
    url(r"linguaskill/lista/$", login_required(MatriculaLinguaskillListView.as_view()), name="matricula_linguaskill_lista"),
    url(r'linguaskill/(?P<venue>\w+)/nueva/$',MatriculaLinguaskillCreateView.as_view(), name="matricula_linguaskill_nueva"),
    url(r'linguaskill/edit/(?P<pk>\d+)/$',login_required(MatriculaLinguaskillUpdateView.as_view()), name="matricula_linguaskill_editar"),
    url(r'linguaskill/gracias/$',MatriculaLinguaskillGracias.as_view(), name="matricula_linguaskill_gracias"),
    url(r'linguaskill/error/$',MatriculaLinguaskillError.as_view(), name="matricula_linguaskill_error"),
    url(r'linguaskill/pagar/(?P<pk>\d+)/$',MatriculaLinguaskillPayView.as_view(), name="matricula_linguaskill_pagar"),
    ## CURSOS ONLINE
    url(r'curso/$',CursoListViewPublica.as_view(), name="curso_online_lista_publica"),
    url(r"curso/curso/lista/$", login_required(CursoListView.as_view()), name="curso_online_lista"),
    url(r'curso/curso/nuevo/$',login_required(CursoCreateView.as_view()), name="curso_online_nuevo"),
    url(r'curso/pagar/(?P<pk>\d+)/$',MatriculaCursoPayView.as_view(), name="matricula_curso_online_pagar"),
    url(r'curso/nueva/(?P<curso_online_id>\d+)/$',MatriculaCursoDirectaCreateView.as_view(), name="matricula_curso_online_directo_nueva"),
    url(r'curso/nueva/$',MatriculaCursoCreateView.as_view(), name="matricula_curso_online_nueva"),
    url(r'curso/gracias/$',MatriculaCursoGracias.as_view(), name="matricula_curso_online_gracias"),
    url(r'curso/error/$',MatriculaCursoError.as_view(), name="matricula_curso_online_error"),
    url(r"curso/matriculas/lista/$", login_required(MatriculaCursoListView.as_view()), name="matricula_curso_online_lista"),
    url(r'curso/matricula/ver/(?P<pk>\d+)/$',login_required(MatriculaCursoDetailView.as_view()), name="matricula_curso_online_detalle"),
    url(r'curso/matricula/editar/(?P<pk>\d+)/$',login_required(MatriculaCursoUpdateView.as_view()), name="matricula_curso_online_editar"),
    
    ## Matriculas EIDE
    url(r"eide/lista/$", login_required(MatriculaEideListView.as_view()), name="matricula_eide_lista"),
    url(r'eide/nueva/$',MatriculaEideCreateView.as_view(), name="matricula_eide_nueva"),
    url(r'eide/gracias/$',MatriculaEideGracias.as_view(), name="matricula_eide_gracias"),
    url(r'eide/error/$',MatriculaEideError.as_view(), name="matricula_eide_error"),
    url(r'eide/ver/(?P<pk>\d+)/$',login_required(MatriculaEideDetailView.as_view()), name="matricula_eide_detalle"),
    url(r'eide/editar/(?P<pk>\d+)/$',login_required(MatriculaEideUpdateView.as_view()), name="matricula_eide_editar"),
    url(r'eide/pagar/(?P<pk>\d+)/$',MatriculaEidePayView.as_view(), name="matricula_eide_pagar"),
    
]
