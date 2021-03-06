# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-22 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0052_auto_20180922_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoNotasParciales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('nombre', models.CharField(max_length=25)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notas_parciales', to='gestioneide.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='NotaParcial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Asistencia')),
                ('grupo_notas_parciales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.GrupoNotasParciales')),
            ],
        ),
    ]
