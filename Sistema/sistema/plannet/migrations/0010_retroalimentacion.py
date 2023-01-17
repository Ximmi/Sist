# Generated by Django 4.0.4 on 2023-01-16 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0009_requerimientos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retroalimentacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.IntegerField(blank=True, null=True, verbose_name='Calificación')),
                ('comentario', models.CharField(blank=True, max_length=50, null=True, verbose_name='Retroalimentación')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_Retroalimentacion', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_Retroalimentacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
