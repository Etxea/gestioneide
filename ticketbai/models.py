# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TicketBai_Ticket(models.Model):
    IDVersionTBAI = models.CharField(max_length=4,default="1.2")
    Emisor_NIF = models.CharField('NIF Emisor',max_length=9,default='B12345678')
    Emisor_ApellidosNombreRazonSocial = models.CharField('Razón Social Emisor',max_length=255,default="ESCUELAS INTERNACIONALES E.I.D.E.  S.L.")
    Destinatarios_NIF = models.CharField('NIF Destinatario',max_length=9,default='B12345678')
    Destinatarios_ApellidosNombreRazonSocial = models.CharField('Razón Social Destinatario',max_length=255,default="ESCUELAS INTERNACIONALES E.I.D.E.  S.L.")
    Factura_SerieFactura = models.CharField('Serie Factura',max_length=5,default='A2000')
    Factura_NumFactura = models.CharField('Num. Factura',max_length=5,default='00001')
    Factura_FechaExpedicionFactura = models.DateField('Fecha',auto_now_add=True)
    Factura_HoraExpedicionFactura = models.TimeField('Hora',auto_now_add=True)
    DatosFactura_DescripcionFactura = models.CharField('Descripción Factura',max_length=255,default="Curso Idiomas")
    DatosFactura_ImporteTotalFactura = models.CharField('Importe Total',max_length=8,default='99999.99')
    enviada = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s/%s"%(self.Factura_SerieFactura,self.Factura_NumFactura)
    
    def __str__(self):
        return self.__unicode__()

    def get_qr_code(self):
        return "https://es.qr-code-generator.com/wp-content/themes/qr/new_structure/assets/media/images/api_page/qrcodes/bw/Api_page_-_QR-Code-Generator_com-1.png"        
    
    def enviar(self):
        todo_bien = True
        if todo_bien:
            self.enviada = True
            self.save()
    
    def general_xml(self):
        return "<xml></xml>"            