# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'pagar/(?P<type>\w+)/(?P<pk>\d+)/$',MatriculaPayView.as_view(), name="matricula_pagar"),
    url(r"venue/lista/$", login_required(VenueListView.as_view()), name="venue_lista"),
    url(r'venue/nueva/$',login_required(VenueCreateView.as_view()), name="venue_nueva"),
    url(r"linguaskill/lista/$", login_required(MatriculaLinguaskillListView.as_view()), name="matricula_linguaskill_lista"),
    url(r'linguaskill/(?P<venue>\w+)/nueva/$',MatriculaLinguaskillCreateView.as_view(), name="matricula_linguaskill_nueva"),
    url(r'linguaskill/gracias/$',MatriculaLinguaskillGracias.as_view(), name="matricula_linguaskill_gracias"),
    url(r'linguaskill/error/$',MatriculaLinguaskillError.as_view(), name="matricula_linguaskill_error"),
    url(r'linguaskill/pagar/(?P<pk>\d+)/$',MatriculaLinguaskillPayView.as_view(), name="matricula_linguaskill_pagar"),
    url(r"eide/lista/$", login_required(MatriculaEideListView.as_view()), name="matricula_eide_lista"),
    url(r'eide/nueva/$',MatriculaEideCreateView.as_view(), name="matricula_eide_nueva"),
    url(r'eide/gracias/$',MatriculaEideGracias.as_view(), name="matricula_eide_gracias"),
    url(r'eide/error/$',MatriculaEideError.as_view(), name="matricula_eide_error"),
    url(r'eide/ver/(?P<pk>\d+)/$',login_required(MatriculaEideDetailView.as_view()), name="matricula_eide_detalle"),
    url(r'eide/editar/(?P<pk>\d+)/$',login_required(MatriculaEideUpdateView.as_view()), name="matricula_eide_editar"),
    url(r'eide/pagar/(?P<pk>\d+)/$',MatriculaEidePayView.as_view(), name="matricula_eide_pagar"),
    
    
]