from django.conf.urls import url
from django.views.generic import TemplateView
from informes.views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r"^$", login_required(TemplateView.as_view(template_name="informes/home.html")), name="informes"),
    url(r"^$", login_required(InformesHomeView.as_view()), name="informes"),
    url(r"profesores/clases/$",login_required(ProfesoresClasesView.as_view()), name="listado_profesores_clases"),

    url(r"aulas/clases/$",login_required(AulasClasesView.as_view()), name="listado_aulas_clases"),

    url(r"alumnos/errores/$",login_required(AlumnosErroresListView.as_view()), name="listado_alumnos_errores"),
    url(r"alumnos/banco/errores/$",login_required(AlumnosBancoErroresListView.as_view()), name="listado_alumnos_banco_errores"),
    url(r"alumnos/mails/errores/xls/$",login_required(export_alumnos_mail_errores_xls), name="listado_alumnos_mail_errores_xls"),
    url(r"alumnos/mail/errores/$",login_required(AlumnosMailErroresListView.as_view()), name="listado_alumnos_mail_errores"),
    
    url(r"alumnos/xls/$",login_required(export_alumnos_xls), name="listado_alumnos_xls"),
    url(r"alumnos/telefonos/xls/(?P<ano>\d+)/$",login_required(export_telefonos_alumnos_xls), name="listado_telefonos_alumnos_xls"),
    #url(r"alumnos/mails/(?P<ano>\d+)/$",login_required(export_mails_alumnos), name="listado_mails_alumnos"),
    
    url(r"asistencias/errores/$",login_required(AsistenciasErroresListView.as_view()), name="listado_asistencias_errores"),
    url(r"asistencias/descuento/$",login_required(AsistenciasDescuentoListView.as_view()), name="listado_asistencias_descuento"),
    url(r"asistencias/metalico/$",login_required(AsistenciasMetalicoListView.as_view()), name="listado_asistencias_metalico"),
    url(r"asistencias/no/xls/$",login_required(export_asistencias_no_confirmadas_xls), name="listado_asistencias_no_confirmadas_xls"),
    url(r"asistencias/xls/$",login_required(export_asistencias_xls), name="listado_asistencias_xls"),
    
    url(r"grupos/xls/$",login_required(export_grupos_xls), name="listado_grupos_xls"),
    url(r"grupos/alumnos/$",login_required(GruposAlumnosListView.as_view()), name="listado_grupos_alumnos"),

    url(r"notas/ano/(?P<ano>\d+)/finales/xls/$",login_required(export_notas_finales_xls), name="listado_notas_finales_ano_xls"),
    url(r"notas/ano/(?P<ano>\d+)/finales/$",login_required(NotasFinalesAnoListView.as_view()), name="listado_notas_finales_ano"),
    url(r"notas/ano/(?P<ano>\d+)/trimestre/$",login_required(NotasTrimestralesAnoListView.as_view()), name="listado_notas_trimestre_ano"),
    url(r"notas/ano/legacy/(?P<ano>\d+)/trimestre/(?P<trimestre>\d+)/$",login_required(NotasTrimestralesLegacyListView.as_view()), name="listado_notas_trimestre_legacy"),
    url(r"notas/ano/(?P<ano>\d+)/cuatrimestre/$",login_required(NotasCuatrimestralesAnoListView.as_view()), name="listado_notas_cuatrimestre_ano"),
    url(r"notas/ano/(?P<ano>\d+)/cuatrimestre/xls/$",login_required(export_notas_cuatrimestre_xls), name="listado_notas_cuatrimestre_xls"),
    url(r"notas/trimestre/(?P<trimestre>\d+)/$",login_required(export_notas_trimestre_xls), name="listado_notas_trimestre"),
    url(r"notas/cuatrimestre/(?P<cuatrimestre>\d+)/$",login_required(export_notas_cuatrimestre_xls), name="listado_notas_cuatrimestre"),

    #~ url(r"notas/$", EvaluacionListView.as_view(template_name="evaluacion/evaluacion_notas.html"), name="evaluacion_notas"),    
]
