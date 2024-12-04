# Generated by Django 5.1.2 on 2024-12-04 00:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_administrador', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='MedioPago',
            fields=[
                ('id_medio_pago', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre_medio_pago', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=100)),
                ('desc_producto', models.CharField(max_length=100)),
                ('precio_unitario', models.FloatField()),
                ('stock', models.IntegerField()),
                ('imagen', models.ImageField(null=True, upload_to='productos/')),
            ],
        ),
        migrations.CreateModel(
            name='Respaldo',
            fields=[
                ('id_respaldo', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_respaldo', models.DateField()),
                ('ubicacion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id_tipo_producto', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre_tipo_producto', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id_detalle_compra', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('valor_total', models.FloatField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.FloatField()),
                ('valor_neto', models.FloatField()),
                ('valor_iva', models.FloatField()),
                ('detalle_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.detallecompra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioValoracion',
            fields=[
                ('id_comentario', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comentario', models.TextField(max_length=300)),
                ('valoracion', models.IntegerField()),
                ('fecha', models.DateField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteVenta',
            fields=[
                ('id_reporte', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo_reporte', models.CharField(max_length=100)),
                ('fecha_reporte', models.DateField()),
                ('total_ventas', models.IntegerField()),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.administrador')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_project.tipoproducto'),
        ),
    ]
