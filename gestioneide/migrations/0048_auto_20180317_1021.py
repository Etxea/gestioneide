# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-03-17 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0047_turismofalta_turismojustificada_turismopresencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='notatrimestral',
            name='aspectos_mejorar',
            field=models.CharField(blank=True, default=b'', max_length=200, null=True, verbose_name=b'Aspectos a mejorar'),
        ),
        migrations.AddField(
            model_name='notatrimestral',
            name='comp_escrita',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name=b'Comprensi\xc3\xb3n Escrita'),
        ),
        migrations.AddField(
            model_name='notatrimestral',
            name='comp_oral',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name=b'Comprensi\xc3\xb3n Oral'),
        ),
        migrations.AddField(
            model_name='notatrimestral',
            name='exp_escrita',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name=b'Expresi\xc3\xb3n Escrita'),
        ),
        migrations.AddField(
            model_name='notatrimestral',
            name='exp_oral',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name=b'Expresi\xc3\xb3n Oral'),
        ),
        migrations.AddField(
            model_name='notatrimestral',
            name='temas_repasar',
            field=models.CharField(blank=True, default=b'', max_length=200, null=True, verbose_name=b'Temas a repasar'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='tipo_evaluacion',
            field=models.DecimalField(choices=[(1, 'Trimestral'), (2, 'Elementary/Pre Intermediate'), (3, 'Intermediate'), (4, 'Upper/[Pre]First/Advance/Proficiency'), (5, 'Kids')], decimal_places=0, max_digits=1),
        ),
    ]
