# Generated by Django 4.0.4 on 2022-06-07 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0015_materiales_alter_contenidoestados_id_estado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingresos',
            name='ingresos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ingresos por año'),
        ),
        migrations.AddField(
            model_name='materiales',
            name='costo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Costo por unidad'),
        ),
        migrations.AddField(
            model_name='materiales',
            name='costo_anual',
            field=models.IntegerField(blank=True, null=True, verbose_name='Costo por año'),
        ),
        migrations.AddField(
            model_name='materiales',
            name='id_estado',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_Materiales', to='plannet.estadosfinancieros'),
        ),
        migrations.AddField(
            model_name='materiales',
            name='id_usuario',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_Materiales', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='materiales',
            name='volumen',
            field=models.IntegerField(blank=True, null=True, verbose_name='Volumen requerido'),
        ),
        migrations.AlterField(
            model_name='materiales',
            name='unidad_medida',
            field=models.CharField(blank=True, choices=[('1', 'Pieza'), ('2', 'Caja'), ('3', 'Barril'), ('4', 'Litro'), ('5', 'Kilogramo'), ('6', 'Paquete')], default=1, max_length=1, null=True),
        ),
        migrations.CreateModel(
            name='ManoObra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre del puesto')),
                ('numero_trabajadores', models.IntegerField(blank=True, null=True, verbose_name='Número de trabajadores')),
                ('pago_mensual', models.IntegerField(blank=True, null=True, verbose_name='Pago mensual')),
                ('pago_anual', models.IntegerField(blank=True, null=True, verbose_name='Pago anual')),
                ('prestaciones', models.IntegerField(blank=True, null=True, verbose_name='Prestaciones 30%')),
                ('total_anual', models.IntegerField(blank=True, null=True, verbose_name='Total anual')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_ManoObra', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_ManoObra', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GastoVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gasto_venta', models.CharField(blank=True, max_length=50, null=True, verbose_name='Descripción del gastode venta')),
                ('unidad', models.CharField(blank=True, max_length=50, null=True, verbose_name='Unidad de medida')),
                ('gasto_unidad', models.IntegerField(blank=True, null=True, verbose_name='Gasto por unidad')),
                ('cantidad', models.IntegerField(blank=True, null=True, verbose_name='Cantidad requerida')),
                ('gasto_anual', models.IntegerField(blank=True, null=True, verbose_name='Gasto por año')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_GastoVenta', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_GastoVenta', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GastoAdministracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre del puesto')),
                ('numero_personas', models.IntegerField(blank=True, null=True, verbose_name='Número de personas')),
                ('pago_mensual', models.IntegerField(blank=True, null=True, verbose_name='Pago mensual')),
                ('pago_anual', models.IntegerField(blank=True, null=True, verbose_name='Pago anual')),
                ('prestaciones', models.IntegerField(blank=True, null=True, verbose_name='Prestaciones 30%')),
                ('total_anual', models.IntegerField(blank=True, null=True, verbose_name='Total anual')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_GastoAdministracion', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_GastoAdministracion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoResultados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo_ventas', models.IntegerField(blank=True, null=True, verbose_name='Costo de ventas')),
                ('materias_primas', models.IntegerField(blank=True, null=True, verbose_name='Materias Primas')),
                ('mano_obra', models.IntegerField(blank=True, null=True, verbose_name='Mano de obra')),
                ('utilidad_bruta', models.IntegerField(blank=True, null=True, verbose_name='Utilidad bruta')),
                ('gastos_generales', models.IntegerField(blank=True, null=True, verbose_name='Gastos generales')),
                ('gastos_administracion', models.IntegerField(blank=True, null=True, verbose_name='Gastos de administración')),
                ('gastos_venta', models.IntegerField(blank=True, null=True, verbose_name='Gastos de venta')),
                ('utilidad_antes_impuestos', models.IntegerField(blank=True, null=True, verbose_name='Utiidad antes de impuestos')),
                ('impuesto', models.IntegerField(blank=True, null=True, verbose_name='Impuesto a la utilidad')),
                ('utilidad_neta', models.IntegerField(blank=True, null=True, verbose_name='Utilidad neta')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_EstadoResultados', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_EstadoResultados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Envase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_envase', models.CharField(blank=True, choices=[('1', 'Envase'), ('2', 'Empaque'), ('3', 'Embalaje')], default=1, max_length=1, null=True)),
                ('volumen', models.IntegerField(blank=True, null=True, verbose_name='Volumen de productos')),
                ('necesidad', models.IntegerField(blank=True, null=True, verbose_name='Necesidad de envase')),
                ('costo', models.IntegerField(blank=True, null=True, verbose_name='Costo unitario')),
                ('costo_anual', models.IntegerField(blank=True, null=True, verbose_name='Costo anual')),
                ('id_estado', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Estado_Envase', to='plannet.estadosfinancieros')),
                ('id_usuario', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Usuario_Envase', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
