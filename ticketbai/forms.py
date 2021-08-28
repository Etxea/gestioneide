# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ticketbai.models import *

class TicketBaiForm(ModelForm):
	class Meta:
		fields = '__all__'
		model = TicketBai_Ticket
		widgets = {'enviada': HiddenInput(),
			'IDVersionTBAI': HiddenInput(),
			'Factura_FechaExpedicionFactura': HiddenInput(),
			'Factura_HoraExpedicionFactura': HiddenInput(),
			}
	
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.add_input(Submit('submit', 'Submit'))
		self.helper.form_class = 'blueForms'
		super(TicketBaiForm, self).__init__(*args, **kwargs)
		self.fields['Factura_SerieFactura'].initial = 'A%s'%datetime.today().year
		last = TicketBai_Ticket.objects.filter(Factura_SerieFactura='A%s'%datetime.today().year).order_by("Factura_NumFactura").last()
		last_num = int(last.Factura_NumFactura)
		self.fields['Factura_NumFactura'].initial = "%05d"%(last_num+1)