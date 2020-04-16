# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-04-15 08:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestioneide', '0065_auto_20200403_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnotacionGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('texto', models.CharField(default=b'', max_length=1000)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Grupo')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
    ]
