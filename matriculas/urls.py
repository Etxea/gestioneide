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
    url(r'linguaskill/edit/(?P<pk>\d+)/$',login_required(MatriculaLinguaskillUpdateView.as_view()), name="matricula_linguaskill_editar"),
    url(r'linguaskill/gracias/$',MatriculaLinguaskillGracias.as_view(), name="matricula_linguaskill_gracias"),
    url(r'linguaskill/error/$',MatriculaLinguaskillError.as_view(), name="matricula_linguaskill_error"),
    url(r'linguaskill/pagar/(?P<pk>\d+)/$',MatriculaLinguaskillPayView.as_view(), name="matricula_linguaskill_pagar"),
    url(r"curso/curso/lista/$", login_required(CursoListView.as_view()), name="curso_lista"),
    url(r'curso/curso/nuevo/$',login_required(CursoCreateView.as_view()), name="curso_nueva"),
    url(r"curso/lista/$", login_required(MatriculaCursoListView.as_view()), name="matricula_curso_lista"),
    url(r'curso/nueva/$',MatriculaCursoCreateView.as_view(), name="matricula_curso_nueva"),
    url(r'curso/(?P<curso>\d+)/nueva/$',MatriculaCursoCreateView.as_view(), name="matricula_curso_directo_nueva"),
    url(r'curso/gracias/$',MatriculaCursoGracias.as_view(), name="matricula_curso_gracias"),
    url(r'curso/error/$',MatriculaCursoError.as_view(), name="matricula_curso_error"),
    url(r'curso/ver/(?P<pk>\d+)/$',login_required(MatriculaCursoDetailView.as_view()), name="matricula_curso_detalle"),
    url(r'curso/editar/(?P<pk>\d+)/$',login_required(MatriculaCursoUpdateView.as_view()), name="matricula_curso_editar"),
    url(r'eide/pagar/(?P<pk>\d+)/$',MatriculaCursoPayView.as_view(), name="matricula_curso_pagar"),
    url(r"eide/lista/$", login_required(MatriculaEideListView.as_view()), name="matricula_eide_lista"),
    url(r'eide/nueva/$',MatriculaEideCreateView.as_view(), name="matricula_eide_nueva"),
    url(r'eide/gracias/$',MatriculaEideGracias.as_view(), name="matricula_eide_gracias"),
    url(r'eide/error/$',MatriculaEideError.as_view(), name="matricula_eide_error"),
    url(r'eide/ver/(?P<pk>\d+)/$',login_required(MatriculaEideDetailView.as_view()), name="matricula_eide_detalle"),
    url(r'eide/editar/(?P<pk>\d+)/$',login_required(MatriculaEideUpdateView.as_view()), name="matricula_eide_editar"),
    url(r'eide/pagar/(?P<pk>\d+)/$',MatriculaEidePayView.as_view(), name="matricula_eide_pagar"),
    url(r'cambridge/list/$',login_required(RegistrationListView.as_view()), name="cambridge_list"),
    url(r'cambridge/list/all$',login_required(RegistrationListViewAll.as_view()), name="cambridge_list_all"),
    url(r'cambridge/excel/$',RegistrationExcelView, name="cambridge_excel"),
    url(r'cambridge/pay/(?P<pk>\d+)/$',RegistrationPayment,name="cambridge_pay"),
    url(r'cambridge/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Registration,
            success_url = '/cambridge/list',
            form_class = RegistrationEditForm,
            template_name='cambridge/registration_edit.html')), name="cambridge_edit"),
    url(r'cambridge/delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Registration,
            success_url="/cambridge/list/")), name="cambridge_delete"),
    url(r'cambridge/view/(?P<pk>\d+)/$', ver, name="cambridge_view"),
    url(r'cambridge/print/(?P<pk>\d+)/$', imprimir_cambridge, name="cambridge_imprimir"),
    url(r'cambridge/new/(?P<exam_id>\d+)/$',RegistrationExamCreateView.as_view(), name="cambridge_nueva_examen"),
    url(r'cambridge/new/$',RegistrationCreateView.as_view(), name="cambridge_nueva"),
    
    #Colegios
    url(r'cambridge/schools/exam/list/$', login_required(SchoolExamList.as_view()),name="cambridge_schools_exam_list"),
    url(r'cambridge/schools/exam/(?P<school_name>\w+)/new/$', login_required(SchoolExamCreate.as_view()),name="cambridge_schools_exam_new"),
    url(r'cambridge/schools/list/$', login_required(SchoolListView.as_view()),name="cambridge_schools_list"),
    url(r'cambridge/schools/registrations/list/$', login_required(SchoolRegistrationListView.as_view()),name="cambridge_schools_registration_list"),
    url(r'cambridge/schools/new/(?P<school_name>\w+)/(?P<school_password>\w+)/$', SchoolRegistrationCreateView.as_view(),name="cambridge_schools_new_registration"),
    url(r'schools/new/$', SchoolCreateView.as_view(),name="cambridge_schools_new"),
    url(r'cambridge/berriotxoa/$', TemplateView.as_view( template_name = 'cambridge/berriotxoa.html' ),name="cambridge_berriotxoa"),
    url(r'cambridge/schools/fuentefresnedo/$', TemplateView.as_view( template_name =  'cambridge/fuentefresnedo.html' ),name="cambridge_fuentefresnedo"),

    #Venues
    url(r'cambridge/venue/exam/list/$', login_required(VenueExamList.as_view()),name="cambridge_venues_exam_list"),
    url(r'cambridge/venue/exam/new/$', login_required(VenueExamCreate.as_view()),name="cambridge_venues_exam_new"),
    url(r'cambridge/venue/list/$', login_required(VenueListView.as_view()),name="cambridge_venues_list"),
    url(r'cambridge/venue/registrations/list/$', login_required(VenueRegistrationListView.as_view()),name="cambridge_venues_registration_list"),
    url(r'cambridge/venue/new/(?P<venue_name>\w+)/$', VenueRegistrationCreateView.as_view(),name="cambridge_venues_new_registration"),
    

    ## Genericas
    url(r'cambridge/thanks/$', TemplateView.as_view( template_name = 'cambridge/gracias.html' ),name="cambridge_gracias"),
    url(r'cambridge/error/$', TemplateView.as_view( template_name = 'cambridge/error.html' ),name="cambridge_error"),
    ##For the exams
    url(r'cambridge/exam/list/$',login_required(
		ListView.as_view(model=Exam,template_name='cambridge/exam_list.html')
		), name="cambridge_exam_list"),
    url(r'cambridge/exam/delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Exam,
            success_url="/cambridge/exam/list/")), name="cambridge_exam_delete"),
    url(r'cambridge/exam/new/$', login_required(
        CreateView.as_view(
            model=Exam,
            form_class = ExamForm,
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_form.html')), name="cambridge_exam_new"),
    url(r'cambridge/exam/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Exam,
            fields = '__all__',
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_edit.html')), name="cambridge_exam_edit"),
    url(r'cambridge/exam/view/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=Exam,
            template_name='cambridge/exam_view.html')), name="cambridge_exam_view"),            
    url(r'cambridge//?$', IndexExamList.as_view(),name="cambridge"),
    
    
]