# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-09 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0012_auto_20160406_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='direccion',
            field=models.CharField(blank=True, default=b'', max_length=250, null=True),
        ),
    ]