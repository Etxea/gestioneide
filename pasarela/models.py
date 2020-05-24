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
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import hashlib
import datetime
#from django.utils.text import slugify
from django.template.defaultfilters import slugify
from cambridge.models import Registration
from django.core.mail import send_mail, mail_admins

import logging
log = logging.getLogger("MatriculaEIDE")



class Pago(models.Model):
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.CharField(_('Concepto'),max_length=250,blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_pago = models.DateField(null=True,blank=True)
    def get_absolute_url(self):
        return "/pagos/pago/%i/" % self.id
    def set_as_paid(self):
        log.debug("Vamos a marcar como pagado el pago: %s con la descripcion %s"%(self.id,self.descripcion))
        self.fecha_pago = datetime.date.today()
        log.debug("Mandamos un mail de confirmacion")
        self.send_paiment_confirmation_email()
        log.debug("Guardamos...")
        self.save()
        return True
    def send_paiment_confirmation_email(self):
		subject = "[PagosOnline] Se ha confirmado un pago manual online"
		message_body = u"""Se acaba de confirmar un pago online creado manualmente. Los datos son: \n
        \tid: %s. \n 
        \tfecha creacion: %s. \n 
        \tdescripcion: %s. \n 
        \timporte: %s. \n 
"""%(self.id,self.fecha_creacion,self.descripcion,self.importe)
		mail_admins(subject, message_body)

