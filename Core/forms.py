from django import forms
from django.forms import ModelForm
from .models import Ciudad, Cliente, CuentaCobrar, CuentaCobrarCuota, CuentaCobrarPago
from datetime import datetime

# CiudadForm
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ('descripcion', 'estado')

# ClienteForm
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            'nombre': 'Nombre del cliente',
            'cedula': 'Cédula',
            'foto': 'Foto del cliente',
            'email': 'Correo electrónico',
            'ciudad': 'Ciudad',
            'sexo': 'Sexo',
            'cupo': 'Cupo',
            'estado': 'Estado'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

# CuentaCobrarForm
class CuentaCobrarForm(ModelForm):
    class Meta:
        model = CuentaCobrar
        fields = ('cliente', 'fecha_credito', 'credito', 'saldo', 'numero_pagos', 'cuota', 'motivo', 'fecha_primer_pago', 'estado')
        labels= {'motivo' : 'Referencia'}

        widgets = {
            'fecha_credito': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs= {'class': 'form-control', 'value': datetime.now().strftime('%Y-%m-%d'),'type':'date'}
            ),

            'fecha_primer_pago': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs= {'class': 'form-control', 'value': datetime.now().strftime('%Y-%m-%d'),'type':'date'}
            ),

            'cuota' : forms.TextInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'}
            ),
        }

# CuentaCobrarCuotaForm
class CuentaCobrarCuotaForm(forms.ModelForm):
    class Meta:
        model = CuentaCobrarCuota
        fields = ('cuenta_cobrar', 'fecha_pagar', 'cuota', 'estado')

# CuentaCobrarPagoForm
class CuentaCobrarPagoForm(forms.ModelForm):
    class Meta:
        model = CuentaCobrarPago
        fields = ('cuenta_cobrar_cuota', 'fecha_pago', 'valor')