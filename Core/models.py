from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User


# MODELS BASE

genero = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)

class Ciudad(models.Model):
    descripcion = models.CharField("Descripcion",max_length=50)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)

    def __str__(self):
        return f'{self.id} - {self.descripcion}'

class Cliente(models.Model):
    nombre = models.CharField("Cliente",max_length=50)
    cedula = models.CharField("Cedula",max_length=10)
    foto = models.FileField(upload_to='clientes/fotos', null=True, blank=True)
    email = models.EmailField("Correo")
    ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT,null=True,blank=True)
    sexo = models.CharField("Sexo", choices=genero, default=genero[0][0], max_length=1)
    cupo = models.DecimalField("Cupo",max_digits=10,decimal_places=2,default=Decimal(0))
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)
    
    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.foto:
            return '{}{}'.format(settings.MEDIA_URL, self.foto)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.jpg')

    
    
#MODELS COBROS

estado_pago = (
    ('PA', 'Pagado'),
    ('PE', 'Pediente'),
)

class CuentaCobrar(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    fecha_credito = models.DateField(default=now)
    credito = models.DecimalField("credito",max_digits=10,decimal_places=2,default=Decimal(0))
    saldo = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal(0))
    numero_pagos = models.IntegerField(default=3)
    cuota = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    motivo = models.CharField(max_length=200)
    fecha_primer_pago = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=2, choices=estado_pago,default=estado_pago[0][0])

    class Meta:
        verbose_name = "Cuenta por Cobrar"
        verbose_name_plural = "Cuentas por Cobrar"

    def __str__(self):
        return '{}'.format(self.credito)


class CuentaCobrarCuota(models.Model):
    ESTADO_PENDIENTE = 0
    ESTADO_PAGADO = 1
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PAGADO, 'Pagado'),
    ]
    cuenta_cobrar = models.ForeignKey(CuentaCobrar, on_delete=models.CASCADE)
    fecha_pagar = models.DateField('Fecha Pagar',blank=True, null=True)
    cuota = models.DecimalField("Couta", max_digits=10, decimal_places=2)
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    
    class Meta:
        verbose_name = "Cuenta x Cobrar detalle"
        verbose_name_plural = "Cuentas x Cobrar detalle"

    def __str__(self):
        return '{}'.format(self.fecha_pagar)


class CuentaCobrarPago(models.Model):
    cuenta_cobrar_cuota = models.ForeignKey(CuentaCobrarCuota, on_delete=models.CASCADE)
    fecha_pago = models.DateField('Fecha Pago',default=now)
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Cuenta x Cobrar Pago"
        verbose_name_plural = "Cuentas x Cobrar Pago"

    def __str__(self):
        return '{}'.format(self.fecha_pago)
