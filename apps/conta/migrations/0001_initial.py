# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 05:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('girocomercial', '0002_initial_data'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unidad', models.FloatField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(verbose_name='número')),
                ('neto', models.FloatField()),
                ('iva', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(verbose_name='número')),
                ('neto', models.FloatField()),
                ('iva', models.FloatField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='conta.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='PersonaJuridica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('razon_social', models.CharField(blank=True, max_length=300)),
                ('rut', models.CharField(max_length=25, unique=True)),
                ('direccion', models.CharField(max_length=300, verbose_name='dirección')),
                ('telefono', models.CharField(max_length=30, verbose_name='teléfono')),
                ('contacto', models.CharField(blank=True, default='', max_length=500)),
                ('url', models.URLField(blank=True, default='', verbose_name='página web')),
                ('giro', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='girocomercial.Giro')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, max_length=1000)),
                ('precio_compra', models.FloatField()),
                ('precio_venta', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona_juridica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='como_proveedor', to='conta.PersonaJuridica')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='documentoventa',
            name='tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='conta.TipoDocumento'),
        ),
        migrations.AddField(
            model_name='documentoproveedor',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='conta.Proveedor'),
        ),
        migrations.AddField(
            model_name='documentoproveedor',
            name='tipo_documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='conta.TipoDocumento'),
        ),
        migrations.AddField(
            model_name='detalledocumento',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='conta.Producto'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='persona_juridica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='como_cliente', to='conta.PersonaJuridica'),
        ),
        migrations.AlterUniqueTogether(
            name='documentoventa',
            unique_together=set([('tipo_documento', 'numero')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentoproveedor',
            unique_together=set([('tipo_documento', 'proveedor', 'numero')]),
        ),
    ]
