# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2019-06-05 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0054_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='ano_activo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Year'),
        ),
    ]
