# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-14 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0015_auto_20160411_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='ciudad',
            field=models.CharField(default=b'Santurtzi', max_length=25),
        ),
    ]
