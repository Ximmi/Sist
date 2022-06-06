# Generated by Django 4.0.4 on 2022-06-06 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0007_alter_coach_options_alter_emprendedor_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupos',
            name='clave',
            field=models.CharField(max_length=50, null=True, verbose_name='Clave'),
        ),
        migrations.AlterField(
            model_name='grupos',
            name='id_integrante',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Integrante', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grupos',
            name='id_responsable',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Responsable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grupos',
            name='nombre_grupo',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre grupo'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='clave_institucion',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='Clave de institucion'),
        ),
    ]
