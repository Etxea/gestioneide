# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.dates import MONTHS
import re


def csb19_normalizar(campo,longitud):
    """Funcion que normaliza el campo: Lo pasa a mayúsculas, lo recorta
        a la longitud si hace falta o lo rellena con espacios hasta la longitud"""
    campo = str(campo)
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
    return str(numero)


def validar_ccc(value):
    if len(value) != 24:
        return False
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


