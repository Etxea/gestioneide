# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

from django import forms
from django.forms import ModelForm
from ticketbai.models import *

class TicketBaiForm(ModelForm):
	class Meta:
		fields = '__all__'
		model = TicketBai_Ticket
	
	def __init__(self, *args, **kwargs):
		super(TicketBaiForm, self).__init__(*args, **kwargs)
		self.fields['Factura_SerieFactura'].initial = 'A%s'%datetime.today().year
		last = TicketBai_Ticket.objects.filter(Factura_SerieFactura='A%s'%datetime.today().year).order_by("Factura_NumFactura").last()
		last_num = int(last.Factura_NumFactura)
		self.fields['Factura_NumFactura'].initial = "%05d"%(last_num+1)