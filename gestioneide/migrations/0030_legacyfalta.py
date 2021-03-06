# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-17 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0029_nota_fecha_creacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyFalta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faltas', models.DecimalField(decimal_places=0, max_digits=3)),
                ('justificadas', models.DecimalField(decimal_places=0, max_digits=3)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Asistencia')),
            ],
        ),
    ]
