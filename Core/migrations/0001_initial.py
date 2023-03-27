# Generated by Django 4.1.7 on 2023-03-25 01:43

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50, verbose_name='Descripcion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de creación')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Cliente')),
                ('cedula', models.CharField(max_length=10, verbose_name='Cedula')),
                ('foto', models.FileField(blank=True, null=True, upload_to='clientes/fotos')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('sexo', models.IntegerField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', verbose_name='Sexo')),
                ('cupo', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Cupo')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de creación')),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Core.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaCobrar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_credito', models.DateField(default=django.utils.timezone.now)),
                ('credito', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='credito')),
                ('saldo', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('numero_pagos', models.IntegerField(default=3)),
                ('cuota', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('motivo', models.CharField(max_length=200)),
                ('fecha_primer_pago', models.DateField(blank=True, null=True)),
                ('estado', models.IntegerField(choices=[('PA', 'Pagado'), ('PE', 'Pediente')], default='PA')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Core.cliente')),
            ],
            options={
                'verbose_name': 'Cuenta por Cobrar',
                'verbose_name_plural': 'Cuentas por Cobrar',
            },
        ),
        migrations.CreateModel(
            name='CuentaCobrarCuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pagar', models.DateField(blank=True, null=True, verbose_name='Fecha Pagar')),
                ('cuota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Couta')),
                ('estado', models.IntegerField(choices=[('PA', 'Pagado'), ('PE', 'Pediente')], default='PA')),
                ('cuenta_cobrar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Core.cuentacobrar')),
            ],
            options={
                'verbose_name': 'Cuenta x Cobrar detalle',
                'verbose_name_plural': 'Cuentas x Cobrar detalle',
            },
        ),
        migrations.CreateModel(
            name='CuentaCobrarPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha Pago')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('cuenta_cobrar_cuota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Core.cuentacobrarcuota')),
            ],
            options={
                'verbose_name': 'Cuenta x Cobrar Pago',
                'verbose_name_plural': 'Cuentas x Cobrar Pago',
            },
        ),
    ]