# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-28 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0045_asistencia_borrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historia',
            name='anotacion',
            field=models.CharField(default=b'', max_length=150),
        ),
        migrations.AlterField(
            model_name='historia',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]