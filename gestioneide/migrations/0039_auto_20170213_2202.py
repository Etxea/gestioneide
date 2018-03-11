# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-13 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0038_pruebanivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='tipo_evaluacion',
            field=models.DecimalField(choices=[(1, 'Trimestral'), (2, 'Elementary/Pre Intermediate'), (3, 'Intermediate'), (4, 'Upper/[Pre]First/Advance/Proficiency')], decimal_places=0, max_digits=1),
        ),
    ]