# Generated by Django 4.0.4 on 2023-01-17 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0012_alter_objetivos_mision_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisArquitectura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_DisArquitectura', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_DisArquitectura', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]