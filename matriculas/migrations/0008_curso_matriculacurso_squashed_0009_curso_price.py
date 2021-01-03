# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-18 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [(b'matriculas', '0008_curso_matriculacurso'), (b'matriculas', '0009_curso_price')]

    dependencies = [
        ('matriculas', '0007_auto_20201123_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('condiciones', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MatriculaCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, editable=False, max_length=6, verbose_name='Password')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('surname', models.CharField(max_length=100, verbose_name='Apellido(s)')),
                ('address', models.CharField(max_length=100, verbose_name='Direcci\xf3n')),
                ('location', models.CharField(max_length=100, verbose_name='Localidad')),
                ('postal_code', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='C\xf3digo Postal')),
                ('sex', models.DecimalField(choices=[(1, 'Male'), (2, 'Female')], decimal_places=0, max_digits=1, verbose_name='Sexo')),
                ('birth_date', models.DateField(help_text='Formato: DD-MM-AAAA(dia-mes-a\xf1o)', verbose_name='Fecha Nacm. DD-MM-AAAA')),
                ('telephone', models.CharField(max_length=12, verbose_name='Tel\xe9fono')),
                ('email', models.EmailField(max_length=254)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False, verbose_name='Pagada')),
                ('accept_conditions', models.BooleanField(default=False, verbose_name='Acepto los t\xe9rminos y condiciones descritos a continuaci\xf3n ')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matriculas.Curso')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=5),
            preserve_default=False,
        ),
    ]
