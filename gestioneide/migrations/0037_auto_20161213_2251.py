# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-13 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0036_auto_20161211_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='notatrimestral',
            name='observaciones',
            field=models.CharField(blank=True, default=b'', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='tipo_evaluacion',
            field=models.DecimalField(choices=[(1, 'Trimestral'), (2, 'Elementary/Prei Intermediate'), (3, 'Intermediate'), (4, 'Upper/[Pre]First/Advance/Proficiency')], decimal_places=0, max_digits=1),
        ),
    ]
