from django.contrib import admin
from .models import Cliente, CuentaCobrar, CuentaCobrarCuota, CuentaCobrarPago, Ciudad

admin.site.register(Ciudad)
admin.site.register(Cliente)
admin.site.register(CuentaCobrar)
admin.site.register(CuentaCobrarCuota)
admin.site.register(CuentaCobrarPago)
