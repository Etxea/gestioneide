# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TicketBai_Ticket(models.Model):
    IDVersionTBAI = models.CharField(max_length=4,default="1.2")
    Emisor_NIF = models.CharField(max_length=9,default='B12345678')
    Emisor_ApellidosNombreRazonSocial = models.CharField('Razón Social',max_length=255,default="ESCUELAS INTERNACIONALES E.I.D.E.  S.L.")
    Destinatarios_NIF = models.CharField(max_length=9,default='B12345678')
    Destinatarios_ApellidosNombreRazonSocial = models.CharField('Razón Social',max_length=255,default="ESCUELAS INTERNACIONALES E.I.D.E.  S.L.")
    Factura_SerieFactura = models.CharField(max_length=5,default='A2021')
    Factura_NumFactura = models.CharField(max_length=5,default='00001')
    Factura_FechaExpedicionFactura = models.TimeField(auto_now_add=True)
    Factura_HoraExpedicionFactura = models.TimeField(auto_now_add=True)
    DatosFactura_DescripcionFactura = models.CharField('Descripción Factura Social',max_length=255,default="Cursi Idiomas")
    DatosFactura_ImporteTotalFactura = models.CharField(max_length=8,default='99999.99')
    enviada = models.BooleanField(default=False)