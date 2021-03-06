# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-06-05 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0002_auto_20200531_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmacion',
            name='fecha_respuesta',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='confirmacion',
            name='respuesta_choice',
            field=models.DecimalField(choices=[(1, 'S\xed'), (2, 'S\xed, pero deseo otro horario'), (3, 'No')], decimal_places=0, default=0, max_digits=1, verbose_name='Respuesta'),
        ),
        migrations.AlterField(
            model_name='confirmacion',
            name='respuesta_texto',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Si no va a asistir el curso que viene, por favor, ind\xedquenos por favor la raz\xf3n'),
        ),
    ]
