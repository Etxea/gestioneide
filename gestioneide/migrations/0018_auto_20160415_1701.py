# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0017_auto_20160415_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='libros',
            field=models.ManyToManyField(blank=True, null=True, to='gestioneide.Libro'),
        ),
    ]
