# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-05-26 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestioneide', '0070_auto_20200517_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirmacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta_bool', models.BooleanField()),
                ('respuesta_texto', models.CharField(max_length=1000, verbose_name='Respuesta (1000carac. max.)')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Asistencia')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('texto', models.CharField(max_length=1500, verbose_name='Consulta')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Grupo')),
            ],
            options={
                'ordering': ['fecha_creacion'],
            },
        ),
        migrations.AddField(
            model_name='confirmacion',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.Consulta'),
        ),
    ]
