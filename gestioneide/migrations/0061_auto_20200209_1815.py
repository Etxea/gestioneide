# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-02-09 17:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestioneide', '0060_alumno_email2'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAlumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enviado', models.BooleanField(default=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('titulo', models.CharField(default='', max_length=100)),
                ('mensaje', models.CharField(default='', max_length=500)),
                ('mensaje_html', models.CharField(default='', max_length=500)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.AlterField(
            model_name='alumno',
            name='email2',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='telefono1',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='telefono2',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='razon_social',
            field=models.CharField(default='ESCUELAS INTERNACIONALES E.I.D.E.  S.L.', max_length=255, verbose_name='Razón Social'),
        ),
        migrations.AlterField(
            model_name='notatrimestral',
            name='comp_escrita',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name='Comprensión Escrita'),
        ),
        migrations.AlterField(
            model_name='notatrimestral',
            name='comp_oral',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name='Comprensión Oral'),
        ),
        migrations.AlterField(
            model_name='notatrimestral',
            name='exp_escrita',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name='Expresión Escrita'),
        ),
        migrations.AlterField(
            model_name='notatrimestral',
            name='exp_oral',
            field=models.DecimalField(blank=True, choices=[(0, 'No Aplica'), (1, 'Mejorable'), (2, 'Satisfactorio'), (3, 'Muy Satisfactorio')], decimal_places=0, default=0, max_digits=1, null=True, verbose_name='Expresión Oral'),
        ),
        migrations.AddField(
            model_name='mailalumno',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Alumno'),
        ),
        migrations.AddField(
            model_name='mailalumno',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
