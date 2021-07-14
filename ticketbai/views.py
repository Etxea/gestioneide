# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from ticketbai.models import *
from ticketbai.forms import *

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class TicketBai_TicketListView(ListView):
    model = TicketBai_Ticket
    template_name = "ticketbai/index.html"
    context_object_name = "tickets"

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')    
class TicketBai_TicketCreateView(CreateView):
    model = TicketBai_Ticket
    template_name = "ticketbai/form_ticketbai_ticket.html"
    form_class = TicketBaiForm
    success_url = "/ticketbai/"

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class TicketBai_TicketDetailView(DetailView):
    model = TicketBai_Ticket
    template_name = "ticketbai/ticket_detail.html"