# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0016_auto_20160414_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='curso',
            name='libros',
            field=models.ManyToManyField(null=True, to='gestioneide.Libro'),
        ),
    ]