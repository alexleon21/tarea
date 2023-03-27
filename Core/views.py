from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Cliente, Ciudad, CuentaCobrar, CuentaCobrarCuota, CuentaCobrarPago
from .forms import ClienteForm, CiudadForm, CuentaCobrarForm
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from datetime import datetime
from pprint import pprint  # Agrega esto en la parte superior de tu archivo
from django.contrib.auth.views import LoginView
import json

class MyLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('inicio')

class InicioListView(ListView):
    template_name = 'list.html'
    context_object_name = 'inicio'

    def get_queryset(self):
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ClienteListView(ListView):
    model = Cliente
    template_name = 'Clientes/listado_cliente.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(nombre__icontains=query)
        return queryset
    
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Clientes/cliente.html'
    success_url = reverse_lazy('clientes')
    
class EditarClienteView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Clientes/cliente.html'
    success_url = reverse_lazy('clientes')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'Clientes/eliminar_cliente.html'
    success_url = reverse_lazy('clientes')
    
#CIUDAD

class CiudadListView(ListView):
    model = Ciudad
    template_name = 'Ciudades/listado_ciudad.html'
    context_object_name = 'ciudad'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(nombre__icontains=query)
        return queryset

class CiudadCreateView(CreateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'Ciudades/ciudad.html'
    success_url = reverse_lazy('ciudad')
    
class EditarCiudadView(UpdateView):
    model = Ciudad
    form_class = CiudadForm
    template_name = 'Ciudades/ciudad.html'
    success_url = reverse_lazy('ciudad')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class CiudadDeleteView(DeleteView):
    model = Ciudad
    template_name = 'Ciudades/eliminar_ciudad.html'
    success_url = reverse_lazy('ciudad')
    
    
#Cuenta_x_Cobrar

class CuentaCobrarListView(ListView):
    model = CuentaCobrar
    template_name = 'cuenta_x_cobrar/listado_cuenta_cobrar.html'
    context_object_name = 'cuentas_cobrar'
    paginate_by = 10
    
    def get_queryset(self):
        return super().get_queryset().order_by('cliente__nombre')
    
    def save(self, *args, **kwargs):
        self.actualizar_estado()
        super(CuentaCobrar, self).save(*args, **kwargs)

    def actualizar_estado(self):
        cuotas = self.cuentacobrarcuota_set.all()
        cuenta_pagada = all(cuota.estado == 1 for cuota in cuotas)
        self.estado = 1 if cuenta_pagada else 0
        print(f"actualizar_estado - cuenta_id: {self.id}, cuenta_pagada: {cuenta_pagada}, estado: {self.estado}")
    
class CuentaCobrarCreateView(CreateView):
    model = CuentaCobrar
    form_class = CuentaCobrarForm
    template_name = 'cuenta_x_cobrar/cuenta_cobrar.html'
    success_url = reverse_lazy('cuenta')

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            cuenta_id = self.kwargs.get('pk')

            # código agregado
            if cuenta_id:
                cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
                # actualizando la cuenta con datos recibidos
            else:
                # creando nueva instancia de cuenta
                cuenta = CuentaCobrar(
                    fecha_credito=datetime.strptime(data['fecha_credito'], '%Y-%m-%d').date(),
                    credito=data['credito'],
                    cliente_id=data['cliente'],
                    numero_pagos=data['numero_pagos'],
                    cuota=data['cuota'],
                    fecha_primer_pago=datetime.strptime(data['fecha_primer_pago'], '%Y-%m-%d').date(),
                    saldo=data['saldo'],
                    motivo=data['motivo']
                )
                cuenta.save()

            # Crear pagos
            pagos_data = data['pagos']
            cuenta_pagada = True  # bandera para verificar si todas las cuotas han sido pagadas
            for i, pago_data in enumerate(pagos_data):
                cuota = CuentaCobrarCuota(
                    cuenta_cobrar=cuenta,
                    fecha_pagar = datetime.strptime(pago_data['fecha_pago'], '%d/%m/%Y').date(),
                    cuota=pago_data['cuota'],
                    estado=1 if pago_data['pagado'] else 0  # cambiar el valor del estado según corresponda
                )
                cuota.save()

                # Crear pagos realizados
                if pago_data['pagado']:
                    pago = CuentaCobrarPago(
                        cuenta_cobrar_cuota=cuota,
                        fecha_pago=datetime.now(),
                        valor=pago_data['cuota']
                    )
                    pago.save()
                else:
                    cuenta_pagada = False  # si hay alguna cuota pendiente, la cuenta no está pagada

            # si todas las cuotas han sido pagadas, cambiar el estado de la cuenta a "pagado"
            if cuenta_pagada:
                cuenta.estado = 1
                pprint("Todas las cuotas pagadas")  # Agrega esta línea para depurar
                cuenta.save()
            else:
                cuenta.estado = 0  # si hay alguna cuota pendiente, la cuenta está "pendiente"
                pprint("Al menos una cuota pendiente")  # Agrega esta línea para depurar
                cuenta.save()
                
                pprint(cuenta.estado)

            return JsonResponse({'status': 'success'})
        else:
            return super().post(request, *args, **kwargs)
        
        
class EditarCuentaView(UpdateView):
    model = CuentaCobrar
    form_class = CuentaCobrarForm
    template_name = 'cuenta_x_cobrar/cuenta_cobrar.html'
    success_url = reverse_lazy('cuenta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cuenta_id = self.kwargs.get('pk')
        cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
        cuotas = cuenta.cuentacobrarcuota_set.all()
        context['cuotas'] = cuotas
        return context

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # procesar solicitud ajax para actualizar pagos
            data = json.loads(request.body)
            cuenta_id = self.kwargs.get('pk')
            cuenta = get_object_or_404(CuentaCobrar, id=cuenta_id)
            cuotas = cuenta.cuentacobrarcuota_set.all()

            # actualizar pagos
            for cuota in cuotas:
                pago_id = data.get(f'pago_{cuota.id}')
                if pago_id:
                    pago = get_object_or_404(CuentaCobrarPago, id=pago_id)
                    pago.fecha_pago = datetime.now().date()
                    pago.save()

            # verificar si todas las cuotas están pagadas
            cuenta_pagada = all(cuota.estado == 1 for cuota in cuotas)

            # leer los datos del formulario de la solicitud HTTP
            fecha_credito = data.get('fecha_credito')
            credito = data.get('credito')
            cliente = data.get('cliente')
            numero_pagos = data.get('numero_pagos')
            cuota = data.get('cuota')
            fecha_primer_pago = data.get('fecha_primer_pago')
            saldo = data.get('saldo')
            motivo = data.get('motivo')
            pagos = data.get('pagos')

            # crear el formulario y actualizar la instancia del modelo
            form = self.form_class(data=request.POST, instance=cuenta)
            if form.is_valid():
                cuenta = form.save(commit=False)
                cuenta.fecha_credito = fecha_credito
                cuenta.credito = credito
                cuenta.cliente = cliente
                cuenta.numero_pagos = numero_pagos
                cuenta.cuota = cuota
                cuenta.fecha_primer_pago = fecha_primer_pago
                cuenta.saldo = saldo
                cuenta.motivo = motivo
                cuenta.estado = CuentaCobrar.ESTADO_PAGADA if cuenta_pagada else CuentaCobrar.ESTADO_PENDIENTE
                cuenta.save()

                for pago_data in pagos:
                    cuota_id = pago_data.get('id')
                    if cuota_id:
                        cuota = get_object_or_404(CuentaCobrarCuota, id=cuota_id)
                        cuota.estado = 1 if pago_data.get('pagado') else 0
                        cuota.save()

                        pago = get_object_or_404(CuentaCobrarPago, id=pago_data.get('pago_id'))
                        pago.fecha_pago = datetime.strptime(pago_data.get('fecha_pago'), '%d/%m/%Y').date()
                        pago.cuota = pago_data.get('cuota')
                        pago.save()

                return JsonResponse({'status': 'success'})
            else:
                form = self.form_class(data=request.POST, instance=self.get_object())
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return self.render_to_response(context)
        else:
            return super().post(request, *args, **kwargs)
                
class CuentaDeleteView(DeleteView):
    model = CuentaCobrar
    template_name = 'cuenta_x_cobrar/eliminar_cuenta.html'
    success_url = reverse_lazy('cuenta')