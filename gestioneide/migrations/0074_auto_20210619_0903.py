# Generated by Django 2.2.24 on 2021-06-19 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0073_auto_20210618_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anotacion',
            name='alumno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Alumno'),
        ),
        migrations.AlterField(
            model_name='anotacion',
            name='creador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='anotaciongrupo',
            name='creador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='anotaciongrupo',
            name='texto',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='aula',
            name='centro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Centro'),
        ),
        migrations.AlterField(
            model_name='aula',
            name='pdi',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='centro',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Empresa'),
        ),
        migrations.AlterField(
            model_name='centro',
            name='telefono',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='clase',
            name='aula',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clases', to='gestioneide.Aula'),
        ),
        migrations.AlterField(
            model_name='clase',
            name='profesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clases', to='gestioneide.Profesor'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cuenta_bancaria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.CuentaBancaria'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='razon_social',
            field=models.CharField(default='ESCUELAS INTERNACIONALES E.I.D.E.  S.L.', max_length=255, verbose_name='Razón Social'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='centro',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Centro'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Curso'),
        ),
        migrations.AlterField(
            model_name='mailalumno',
            name='alumno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Alumno'),
        ),
        migrations.AlterField(
            model_name='mailalumno',
            name='creador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
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
        migrations.AlterField(
            model_name='perfil',
            name='ano_activo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Year'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='telefono',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='pruebanivel',
            name='nivel_recomendado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestioneide.Curso'),
        ),
    ]
