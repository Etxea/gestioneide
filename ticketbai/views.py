# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import permission_required
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from ticketbai.forms import *
from ticketbai.models import *


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
    success_url = reverse_lazy('ticketbai_index')

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class TicketBai_TicketDetailView(DetailView):
    model = TicketBai_Ticket
    template_name = "ticketbai/ticket_detail.html"

class TicketBai_TicketPublicDetailView(DetailView):
    model = TicketBai_Ticket
    template_name = "ticketbai/ticket_public_detail.html"

class TicketBai_TicketQrView(TicketBai_TicketPublicDetailView):
    template_name = "ticketbai/ticket_qr.html"        