# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.dates import MONTHS
import re

def csb19_crear_presentador(fecha_confeccion):
    """Funcion que crea el campo presentador y lo añade al contenido"""
    contenido=""
    cod_reg = "51"
    cod_dato = "80"
    relleno_b3 = ' '*6
    relleno_d = ' '*20
    relleno_e3 = ' '*12
    relleno_f = ' '*40
    relleno_g = ' '*14
    cabecera_presentador = cod_reg + cod_dato + settings.NIF + settings.CSB19["sufijo"] + fecha_confeccion + \
        relleno_b3 + settings.CSB19["nombre"] + relleno_d + settings.CSB19["banco"] + settings.CSB19["oficina"] + \
        relleno_e3 + relleno_f + relleno_g + "\r\n"
    contenido += cabecera_presentador
    return contenido
    

def csb19_crear_ordenante(contenido,fecha_confeccion, fecha_cargo):
    """Funcion que crea el campo ordenante y lo añade al contenido"""
    cod_reg = "53"
    cod_dato = "80"
    procedimiento= "01"
    relleno_e1= ' '*8
    relleno_e3= ' '*10
    relleno_f = ' '*40
    relleno_g = ' '*14
    cabecera_ordenante = cod_reg + cod_dato + settings.NIF + settings.CSB19["sufijo"] + fecha_confeccion + fecha_cargo + \
        settings.CSB19["nombre"] + settings.CSB19["banco"] + settings.CSB19["oficina"] + settings.CSB19["dc"] + \
        settings.CSB19["cuenta"] + relleno_e1 + procedimiento + relleno_e3 + relleno_f + relleno_g + '\r\n'
    contenido += cabecera_ordenante
    return contenido
    
def csb19_crear_individual(contenido,importe_recibos,numero_recibos,asistencia,mes,medio_mes):
    ##Recibimos la asistencia y de ella sacamos: id, nombre, CCC, importe y concepto
    id = asistencia.id
    nombre="%s %s"%(asistencia.alumno.apellido1,asistencia.alumno.apellido2)
    ccc=asistencia.alumno.cuenta_bancaria.replace("-","")
    
    if medio_mes:
        importe=float(asistencia.ver_precio())/2
    else:
        importe=asistencia.ver_precio()
    concepto="EIDE: %s, %s"%(asistencia.grupo.nombre,MONTHS[mes])
    #Sumamos el importe al total
    try:
        importe_recibos += float(importe)
    except:
        print "NO hemos podido generar el import para %s %s"%(nombre,importe)
    numero_recibos += 1
    cod_reg = "56"
    cod_dato = "80"
    #relleno de 16
    relleno_f = ' '*16
    #relleno de 8
    relleno_h = ' '*8
    ##Normalizamos (rellenamos) los campos nombre, importe y concepto
    nombre = csb19_normalizar(nombre,40)
    concepto = csb19_normalizar(concepto,40)

    #Vamos con el importe
    importe = csb19_ajustar(importe,10,2)

    individual = cod_reg + cod_dato + settings.NIF + settings.CSB19["sufijo"] + csb19_ajustar(id,12) + nombre + \
        ccc + importe + relleno_f + concepto + relleno_h + '\r\n'
    contenido += individual
    return contenido,importe_recibos,numero_recibos

def csb19_crear_total_ordenante(contenido,numero_recibos,importe_recibos):
    cod_reg  = "58"
    cod_dato = "80"
    relleno_b2 = " "*12
    relleno_c  = " "*40
    relleno_d  = " "*20
    relleno_e2 = " "*6
    relleno_f3 = " "*20
    relleno_g  = " "*18
    ##FIXME ajustar el formato del importe total
    importe_recibos = str(importe_recibos)
    
    total_ordenante = cod_reg + cod_dato + settings.NIF + settings.CSB19["sufijo"] + relleno_b2 \
        + relleno_c + relleno_d + csb19_ajustar(importe_recibos,10,2) + relleno_e2 \
        + csb19_ajustar(numero_recibos,10) + csb19_ajustar(numero_recibos+2,10) + relleno_f3 \
        + relleno_g + '\r\n'
    contenido += total_ordenante
    return contenido

def csb19_crear_total_general(contenido,numero_recibos,importe_recibos):
    cod_reg  = "59"
    cod_dato = "80"
    relleno_b2 = " "*12
    relleno_c  = " "*40
    relleno_d2  = " "*16
    relleno_e2 = " "*6
    relleno_f3 = " "*20
    relleno_g  = " "*18
    num_ordenantes = "0001"
    ##FIXME ajustar el formato del importe total
    importe_recibos = str(importe_recibos)
    total_general = cod_reg + cod_dato + settings.NIF + settings.CSB19["sufijo"] + relleno_b2 +\
        relleno_c + num_ordenantes + relleno_d2 + csb19_ajustar(importe_recibos,10,2) + relleno_e2 + \
        csb19_ajustar(numero_recibos,10) + csb19_ajustar(numero_recibos+4,10) + relleno_f3 + relleno_g  + '\r\n'
    contenido += total_general
    return contenido

def csb19_crear_totales(contenido,numero_recibos,importe_recibos):
    """creamos los totales"""
    contenido = csb19_crear_total_ordenante(contenido,numero_recibos,importe_recibos)
    contenido = csb19_crear_total_general(contenido,numero_recibos,importe_recibos)
    return contenido

def csb19_normalizar(campo,longitud):
    """Funcion que normaliza el campo: Lo pasa a mayúsculas, lo recorta
        a la longitud si hace falta o lo rellena con espacios hasta la longitud"""
    #~ campo = str(campo)
    campo = campo.upper()
    if len(campo)>longitud:
        #recortamos hasta longitud
        campo = campo[0:longitud]
    if len(campo)<longitud:
        #rellenamos hasta lamgitud
        campo += ' '*(longitud-len(campo))
    return campo

def csb19_ajustar(numero,longitud, num_decimales=0):
    """Función que ajusta a la derecha el numero añadiendo por la izquierda los "0" que sean necesario"""
    unidades = str(numero).split('.')[0]
    if num_decimales == 0:
        numero = unidades
    else:
        try:
            decimales = str(numero).split('.')[1]
            decimales = decimales[0:num_decimales]
            decimales = decimales + '0'*(num_decimales-len(decimales))
        except:
            ##print "Añadimos %s 0 como decimales"%num_decimales
            decimales = '0'*num_decimales
        numero = unidades + str(decimales[0:num_decimales])

    if len(numero)<longitud:
##            print "Hacen falta ceros a la izquierda..."
        numero = '0'*(longitud-len(numero))+numero
    return numero


def validar_ccc(value):
    if len(value) != 24:
        return False
    print "Validando la cuenta",value
    m = re.match(r'^(\d{4})[ -]?(\d{4})[ -]?(\d{2})[ -]?(\d{10})$', value)
    entity, office, checksum, account = m.groups()
    if get_checksum('00' + entity + office) + get_checksum(account) == checksum:
        return True
    else:
        return False


def get_checksum(d):
    control_str = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
    digits = [int(digit) * int(control) for digit, control in zip(d, control_str)]
    return str(11 - sum(digits) % 11).replace('10', '1').replace('11', '0')


