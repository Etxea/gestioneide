# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-18 13:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cambridge', '0007_auto_20200210_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='registration_end_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha fin de la matriculaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='linguaskillregistration',
            name='proposed_date',
            field=models.DateField(help_text='Formato: DD-MM-AAAA(dia-mes-a\xf1o)', verbose_name='Fecha propuesta DD-MM-AAAA'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='accept_conditions',
            field=models.BooleanField(default=True, help_text='Doy mi consentimiento expreso para recibir comunicaciones en los t\xe9rminos anteriormente descritos.', verbose_name='Doy mi consentimiento expreso para recibir comunicaciones en los t\xe9rminos anteriormente descritos.'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='accept_photo_conditions',
            field=models.BooleanField(default=True, help_text='Debes aceptar las condiciones de la la toma de foto para poder matricularte.', verbose_name='Doy mi consentimiento expreso para que mi imagen pueda ser utilizada en la p\xe1gina Web o en redes sociales del centro as\xed como en todo el material publicitario que pueda utilizar.'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='address',
            field=models.CharField(max_length=100, verbose_name='Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='birth_date',
            field=models.DateField(help_text='Formato: DD-MM-AAAA(dia-mes-a\xf1o)', verbose_name='Fecha Nacm. DD-MM-AAAA'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='postal_code',
            field=models.DecimalField(decimal_places=0, max_digits=6, verbose_name='C\xf3digo Postal'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='telephone',
            field=models.CharField(max_length=12, verbose_name='Tel\xe9fono'),
        ),
    ]
