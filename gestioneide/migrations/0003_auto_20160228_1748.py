# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 16:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0002_auto_20160223_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='clase',
            name='dia_semana',
            field=models.DecimalField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes')], decimal_places=0, max_digits=1),
        ),
    ]
