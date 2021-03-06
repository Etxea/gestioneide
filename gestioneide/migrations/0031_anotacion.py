# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-20 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0030_legacyfalta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('texto', models.CharField(default=b'', max_length=25)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Alumno')),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
    ]
