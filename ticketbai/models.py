# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse_lazy

from gestioneide.models import Empresa, Alumno


CHOICES_SINO = [('S', 'Sí'),('N', 'No')]

## L2
CHOICES_TIPOID = [
    ('02', 'NIF-IVA'),
    ('03', 'Pasaporte'),
    ('04', 'Doc. oficial pais de residencia'),
    ('05', 'Certificado Residencia'),
    ('06', 'Otro'),
]

CHOICES_REGIMEN_IVA = [
    ('01', 'Régimen general'),
    ('02', 'Exportación'),
    ('03', 'Bienes usados, objectos de arte, antigüedades, colección'),
    ('04', 'Oro'),
    ('05', 'Agencias viajes'),
    ('06', ''),
    ('07', ''),
    ('08', ''),
    ('09', ''),
    ('10', ''),
    ('11', ''),
    ('12', ''),
    ('13', ''),
    ('14', ''),
    ('15', ''),
    ('51', ''),
    ('52', ''),
    ('53', ''),
]

CHOICES_EXENCION_IVA = [
    ('E1', 'Artículo 20 Normal Foral del IVA'),
    ('E2', 'Artículo 21 Normal Foral del IVA'),
    ('E3', 'Artículo 22 Normal Foral del IVA'),
    ('E4', 'Artículo 23 y 24 Normal Foral del IVA'),
    ('E5', 'Artículo 25 Normal Foral del IVA'),
    ('E6', 'otra causa')
]

CHOICES_TIPO_NOEXENTA = [
    ('S1', 'Sin inversión en sujeto pasivo'),
    ('S2', 'Con inversión en sujeto pasivo')
]


CHOICES_CAUSA_NOSUJETA = [
    ('OT', 'Articulo 7'),
    ('RL', 'Reglas Localización')
]

class TicketBai_Ticket(models.Model):
    IDVersionTBAI = models.CharField(max_length=4,default="1.2")
    empresa_emisor = models.ForeignKey(Empresa,on_delete=models.PROTECT)
    alumno_destinatario = models.ForeignKey(Alumno,null=True,on_delete=models.PROTECT)
    Destinatarios_NIF = models.CharField('NIF Destinatario',max_length=9,default='',null=True,blank=True)
    Destinatarios_ApellidosNombreRazonSocial = models.CharField('Razón Social Destinatario',max_length=255,default='',null=True,blank=True)
    Factura_SerieFactura = models.CharField('Serie Factura',max_length=5,default='A2000')
    Factura_NumFactura = models.CharField('Num. Factura',max_length=5,default='00001')
    Factura_FechaExpedicionFactura = models.DateField('Fecha',auto_now_add=True)
    Factura_HoraExpedicionFactura = models.TimeField('Hora',auto_now_add=True)
    FacturaSimplificada = models.CharField(max_length=1,default='S',choices=CHOICES_SINO)
    DatosFactura_RetencionSoportada = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    DatosFactura_DescripcionFactura = models.CharField('Descripción Factura',max_length=255,default="Curso Idiomas")
    DatosFactura_ImporteTotalFactura = models.DecimalField('Importe Total',max_digits=12, decimal_places=2,default=99.99, null=True, blank=True)
    DatosFactura_Claves = models.CharField(max_length=2,default='01',choices=CHOICES_REGIMEN_IVA)
    TipoDesglose_CausaExencion = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES_EXENCION_IVA)
    TipoDesglose_BaseImponible = models.DecimalField('Base Imponible exenta IVA',max_digits=12, decimal_places=2,default=99.99, null=True, blank=True)
    TipoDesglose_Nosujeta_DetalleNoSujeta_Causa = models.DecimalField('Importe no sujeto',max_digits=12, decimal_places=2,default=99.99, null=True, blank=True)
    TipoDesglose_Nosujeta_DetalleNoSujeta_Importe = models.DecimalField('Base Imponible exenta IVA',max_digits=12, decimal_places=2,default=0, null=True, blank=True)
    HuellaTBAI_Encadenamiento_NumFacturaAnterior = models.CharField(max_length=5,blank=True,null=True) 
    HuellaTBAI_Encadenamiento_FechaExpedicionFacturaAnterior = models.DateField(blank=True,null=True)
    HuellaTBAI_Encadenamiento_SignatureValueFirmaFacturaAnterior = models.CharField(max_length=100,blank=True,null=True) 
    HuellaTBAI_Software_LicenciaTBAI = models.CharField(max_length=20,blank=True,null=True) 
    HuellaTBAI_Software_EntidadDesarrolladora_NIF = models.CharField('NIF Desarrollado',max_length=9,default='',null=True,blank=True)
    HuellaTBAI_Software_EntidadDesarrolladora_IDOtro_IDType = models.CharField(max_length=2,blank=True,null=True)
    HuellaTBAI_Software_EntidadDesarrolladora_IDOtro_ID = models.CharField(max_length=20,blank=True,null=True)
    HuellaTBAI_Software_Nombre = models.CharField(max_length=120,blank=True,null=True)
    HuellaTBAI_Software_Version = models.CharField(max_length=20,blank=True,null=True)
    
    enviada = models.BooleanField(default=False)

    def Emisor_NIF(self):
        return self.empresa_emisor.cif

    def Emisor_ApellidosNombreRazonSocial(self):
        return self.empresa_emisor.razon_social

    def __unicode__(self):
        return "%s/%s"%(self.Factura_SerieFactura,self.Factura_NumFactura)
    
    def __str__(self):
        return self.__unicode__()

    def codigo_indentificativo(self):
        return 'TBAI-000000000Y-010122-FFFFFFFFFFFFF-CRC'

    def public_url(self):
        return "https://batuz.eus/QRTBAI/%s&s=T&nf=27174&i=4.70&cr007"%self.codigo_indentificativo()
    
    def save(self):
        #Rellenamos detalles del destinario si es un alumno
        if self.alumno_destinatario:
            self.Destinatarios_ApellidosNombreRazonSocial=self.alumno_destinatario.razon_social()
            self.Destinatarios_NIF=self.alumno_destinatario.dni

        return super().save()

    def enviar(self):
        todo_bien = True
        if todo_bien:
            self.enviada = True
            self.save()
    
    def general_xml(self):
        return "<xml></xml>"            