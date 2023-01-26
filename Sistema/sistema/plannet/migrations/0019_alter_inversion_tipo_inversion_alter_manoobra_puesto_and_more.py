# Generated by Django 4.0.4 on 2023-01-20 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0018_alter_gastoventa_gasto_venta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inversion',
            name='tipo_inversion',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Tipo de inversión'),
        ),
        migrations.AlterField(
            model_name='manoobra',
            name='puesto',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Nombre del puesto'),
        ),
        migrations.AlterField(
            model_name='requerimientos',
            name='Requerimiento',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descripción del requerimiento'),
        ),
        migrations.AlterField(
            model_name='retroalimentacion',
            name='comentario',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Retroalimentación'),
        ),
    ]