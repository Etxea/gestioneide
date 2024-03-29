# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-06-18 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestioneide', '0073_auto_20210618_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default=b'', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencia_turismo', to='gestioneide.Alumno')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turismo.Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.DecimalField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miercoles'), (4, 'Jueves'), (5, 'Viernes')], decimal_places=0, max_digits=1)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases_turismo', to='turismo.Asignatura')),
                ('aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases_turismo', to='gestioneide.Aula')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases_turismo', to='gestioneide.Profesor')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default=b'', max_length=50)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Year')),
            ],
        ),
        migrations.CreateModel(
            name='Falta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.DecimalField(decimal_places=0, max_digits=2)),
                ('dia', models.DecimalField(decimal_places=0, max_digits=2)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turismo.Asistencia')),
            ],
        ),
        migrations.CreateModel(
            name='Justificada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.DecimalField(decimal_places=0, max_digits=2)),
                ('dia', models.DecimalField(decimal_places=0, max_digits=2)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turismo.Asistencia')),
            ],
        ),
        migrations.CreateModel(
            name='Presencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.DecimalField(decimal_places=0, max_digits=2)),
                ('dia', models.DecimalField(decimal_places=0, max_digits=2)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turismo.Asistencia')),
            ],
        ),
        migrations.AddField(
            model_name='asignatura',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaturas', to='turismo.Curso'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Profesor'),
        ),
    ]
