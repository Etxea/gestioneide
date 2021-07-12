# Generated by Django 2.2.24 on 2021-06-19 07:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cambridge', '0008_auto_20210618_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='accept_conditions',
            field=models.BooleanField(blank=True, default=True, help_text='Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.', verbose_name='Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='accept_photo_conditions',
            field=models.BooleanField(blank=True, default=True, help_text='Debes aceptar las condiciones de la la toma de foto para poder matricularte.', verbose_name='Doy mi consentimiento expreso para que mi imagen pueda ser utilizada en la página Web o en redes sociales del centro así como en todo el material publicitario que pueda utilizar.'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='eide_alumn',
            field=models.BooleanField(blank=True, default='False', help_text='Haz click en el check si eres alumno/a de EIDE. En caso contrario rellena porfavor la siguiente casilla.', verbose_name='Alumno EIDE'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='exam',
            field=models.ForeignKey(limit_choices_to={'registration_end_date__gte': datetime.date(2021, 6, 19)}, on_delete=django.db.models.deletion.CASCADE, to='cambridge.Exam'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='minor',
            field=models.BooleanField(blank=True, default=False, verbose_name='El candidato es menor de edad y yo soy su padre/madre o tutor legal.'),
        ),
        migrations.AlterField(
            model_name='school',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='Description'),
        ),
    ]
