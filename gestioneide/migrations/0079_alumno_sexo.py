# Generated by Django 2.2.24 on 2021-10-18 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0078_notaunitswriting'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='sexo',
            field=models.DecimalField(blank=True, choices=[(1, 'Mujer'), (2, 'Hombre')], decimal_places=0, max_digits=1, null=True, verbose_name='Sexo'),
        ),
    ]
