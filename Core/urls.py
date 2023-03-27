from django.urls import path
from django.urls import path, reverse
from .views import ClienteListView, InicioListView, EditarClienteView, ClienteDeleteView, ClienteCreateView, CiudadListView, CiudadCreateView, CiudadDeleteView, EditarCiudadView, CuentaCobrarListView, CuentaCobrarCreateView, CuentaDeleteView, EditarCuentaView, MyLoginView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', MyLoginView.as_view(), name='login'),
    path('inicio/', InicioListView.as_view(), name='inicio'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('clientes/', ClienteListView.as_view(), name='clientes'),
    path('crear_cliente/', ClienteCreateView.as_view(), name='crear_cliente'),
    path('editar_cliente/<int:pk>/', EditarClienteView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),
    
    path('ciudad/', CiudadListView.as_view(), name='ciudad'),
    path('crear_ciudad/', CiudadCreateView.as_view(), name='crear_ciudad'),
    path('editar_ciudad/<int:pk>/', EditarCiudadView.as_view(), name='editar_ciudad'),
    path('eliminar_ciudad/<int:pk>/', CiudadDeleteView.as_view(), name='eliminar_ciudad'),
    
    path('cuenta/', CuentaCobrarListView.as_view(), name='cuenta'),
    path('crear_cuenta/', CuentaCobrarCreateView.as_view(), name='crear_cuentas_cobrar'),
    path('editar_cuenta/<int:pk>/', EditarCuentaView.as_view(), name='editar_cuenta'),
    path('eliminar_cuenta/<int:pk>/', CuentaDeleteView.as_view(), name='eliminar_cuenta'),
       
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)