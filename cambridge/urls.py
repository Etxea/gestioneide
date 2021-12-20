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
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from cambridge.views import *
from cambridge.forms import *
from cambridge.models import *

urlpatterns = [
    url(r'^list/$',login_required(RegistrationListView.as_view()), name="cambridge_list"),
    url(r'^list/all$',login_required(RegistrationListViewAll.as_view()), name="cambridge_list_all"),
    url(r'^list/exam/(?P<exam_id>\d+)/$',login_required(RegistrationListViewExam.as_view()), name="cambridge_list_exam"),
    url(r'^excel/$',login_required(RegistrationExcelView.as_view()), name="cambridge_excel"),
    url(r'^excel/exam/(?P<exam_id>\d+)/$',login_required(RegistrationExcelView.as_view()), name="cambridge_excel_exam"),
    url(r'^pay/(?P<pk>\d+)/$',RegistrationPayment,name="cambridge_pay"),
    url(r'^edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Registration,
            success_url = '/cambridge/list',
            form_class = RegistrationEditForm,
            template_name='cambridge/registration_edit.html')), name="cambridge_edit"),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Registration,
            success_url="/cambridge/list/")), name="cambridge_delete"),
    url(r'^view/(?P<pk>\d+)/$', ver, name="cambridge_view"),
    url(r'^print/(?P<pk>\d+)/$', imprimir_cambridge, name="cambridge_imprimir"),
    url(r'^new/(?P<exam_id>\d+)/$',RegistrationExamCreateView.as_view(), name="cambridge_nueva_examen"),
    url(r'^new/$',RegistrationCreateView.as_view(), name="cambridge_nueva"),
    
    #Colegios
    url(r'schools/exam/list/$', login_required(SchoolExamList.as_view()),name="cambridge_schools_exam_list"),
    url(r'schools/exam/(?P<school_name>\w+)/new/$', login_required(SchoolExamCreate.as_view()),name="cambridge_schools_exam_new"),
    url(r'schools/list/$', login_required(SchoolListView.as_view()),name="cambridge_schools_list"),
    url(r'schools/registrations/list/$', login_required(SchoolRegistrationListView.as_view()),name="cambridge_schools_registration_list"),
    url(r'schools/new/(?P<school_name>\w+)/(?P<school_password>\w+)/$', SchoolRegistrationCreateView.as_view(),name="cambridge_schools_new_registration"),
    url(r'schools/new/$', SchoolCreateView.as_view(),name="cambridge_schools_new"),
    url(r'berriotxoa/$', TemplateView.as_view( template_name = 'cambridge/berriotxoa.html' ),name="cambridge_berriotxoa"),
    url(r'schools/fuentefresnedo/$', TemplateView.as_view( template_name =  'cambridge/fuentefresnedo.html' ),name="cambridge_fuentefresnedo"),

    #Venues
    url(r'venue/exam/list/$', login_required(VenueExamList.as_view()),name="cambridge_venues_exam_list"),
    url(r'venue/exam/new/$', login_required(VenueExamCreate.as_view()),name="cambridge_venues_exam_new"),
    url(r'venue/list/$', login_required(VenueListView.as_view()),name="cambridge_venues_list"),
    url(r'venue/registrations/list/$', login_required(VenueRegistrationListView.as_view()),name="cambridge_venues_registration_list"),
    url(r'venue/new/(?P<venue_name>\w+)/$', VenueRegistrationCreateView.as_view(),name="cambridge_venues_new_registration"),
    
    #Linguaskill
    url(r'linguaskill/new/$', LinguaskillRegistrationCreateView.as_view(),name="cambridge_linguaskill_new_registration"),
    url(r'linguaskill/list/$', LinguaskillRegistrationListView.as_view(),name="cambridge_linguaskill_registration_list"),
    
    ## Prep Center
    url(r'prepcenter/$', PrepCenterHomeView.as_view(),name="cambridge_prepcenter_home"),
    url(r'prepcenter/pay/registrations/$', PrepCenterRegistrationsPayView.as_view(),name="cambridge_prepcenters_registrations_pays"),
    url(r'prepcenter/new/center/$', PrepCenterCreateView.as_view(),name="cambridge_prepcenters_new"),
    url(r'prepcenter/update/center/(?P<pk>\d+)/$', PrepCenterUpdateView.as_view(),name="cambridge_prepcenters_update"),
    url(r'prepcenter/list/$', login_required(PrepCenterListView.as_view()),name="cambridge_prepcenters_list"),
    #url(r'prepcenter/exam/list/$', login_required(PrepCenterExamList.as_view()),name="cambridge_prepcenters_exam_list"),
    # url(r'prepcenter/exam/new/$', PrepCenterExamCreate.as_view(),name="cambridge_prepcenters_exam_new"),
    url(r'prepcenter/registrations/new/$', PrepCenterRegistrationCreateView.as_view(),name="cambridge_prepcenters_registration_new"),
    url(r'prepcenter/registrations/new/exam/(?P<exam_id>\d+)/(?P<form_num>\d+)/$',PrepCenterRegistrationExamCreateView.as_view(),name="cambridge_prepcenters_registration_exam_new"),
    url(r'prepcenter/registrations/new/exam/(?P<exam_id>\d+)/$',PrepCenterRegistrationExamCreateView.as_view(),name="cambridge_prepcenters_registration_exam_new"),
    url(r'prepcenter/registrations/delete/(?P<pk>\d+)/$',PrepCenterRegistrationDeleteView.as_view(), name="prepcenter_registration_delete"),
    #url(r'prepcenter/registrations/list/$', login_required(PrepCenterRegistrationListView.as_view()),name="cambridge_prepcenters_registration_list"),
    url(r'prepcenter/passwordreset/(?P<pk>\d+)/$',PrepCenterPasswordResetView.as_view(), name="prepcenter_passwordreset"),
    url(r'prepcenter/createuser/(?P<pk>\d+)/$',PrepCenterCreateUserView.as_view(), name="prepcenter_createuser"),
    url(r'prepcenter/disableuser/(?P<pk>\d+)/$',PrepCenterDisableUserView.as_view(), name="prepcenter_disableuser"),
    url(r'prepcenter/enableuser/(?P<pk>\d+)/$',PrepCenterEnableUserView.as_view(), name="prepcenter_enableuser"),
    url(r'prepcenter/detalle/(?P<pk>\d+)/$',PrepCenterDetailView.as_view(), name="prepcenter_detalle"),
    url(r'prepcenter/delete/(?P<pk>\d+)/$',PrepCenterDeleteView.as_view(), name="prepcenter_delete"),
    url(r'prepcenter/registrations/pay/(?P<pk>\d+)/$',PrepCenterPayRegistrations.as_view(), name="prepcenter_registrations_admin_pay"),
    
    ## Genericas
    url(r'thanks/$', TemplateView.as_view( template_name = 'cambridge/gracias.html' ),name="cambridge_gracias"),
    url(r'error/$', TemplateView.as_view( template_name = 'cambridge/error.html' ),name="cambridge_error"),
    
    ##For the exams
    url(r'^exam/list/$',login_required(
		ListView.as_view(model=Exam,template_name='cambridge/exam_list.html')
		), name="cambridge_exam_list"),
    url(r'^exam/delete/(?P<pk>\d+)/$',
        login_required(DeleteView.as_view(
            model=Exam,
            success_url="/cambridge/exam/list/")), name="cambridge_exam_delete"),
    url(r'^exam/new/$', login_required(
        CreateView.as_view(
            model=Exam,
            form_class = ExamForm,
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_form.html')), name="cambridge_exam_new"),
    url(r'^exam/edit/(?P<pk>\d+)/$',
        login_required(UpdateView.as_view(
            model=Exam,
            fields = '__all__',
            success_url = '/cambridge/exam/list',
            template_name='cambridge/exam_edit.html')), name="cambridge_exam_edit"),
    url(r'^$', IndexExamList.as_view(),name="cambridge"),
]
