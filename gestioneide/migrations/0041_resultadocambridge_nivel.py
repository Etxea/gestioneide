# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-14 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0040_resultadocambridge'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadocambridge',
            name='nivel',
            field=models.DecimalField(choices=[(1, 'KET'), (2, 'PET'), (3, 'FCE'), (4, 'CAE'), (5, 'CPE')], decimal_places=0, default=1, max_digits=1),
        ),
    ]
