from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.administracion.views.web.cliente_web import cliente_lista, cliente_create, cliente_editar, cliente_eliminar, cliente_detalle_json
from apps.administracion.views.web.marca_web import marca_lista, marca_create, marca_editar, marca_eliminar
from apps.administracion.views.web.combustible_web import combustible_lista, combustible_create, combustible_editar, combustible_eliminar
from apps.administracion.views.web.modelo_web import modelo_lista, modelo_create, modelo_editar, modelo_eliminar
from apps.administracion.views.web.vehiculo_web import vehiculo_lista, vehiculo_create, vehiculo_editar,vehiculo_eliminar
from apps.administracion.views.web.evidencia_web import evidencia_lista, evidencia_create,evidencia_editar,evidencia_eliminar
from apps.administracion.views.web.categoria_servicio_web import categoria_lista, categoria_create, categoria_editar, categoria_eliminar
from apps.administracion.views.web.servicio_web import servicio_lista, servicio_create, servicio_editar, servicio_eliminar
from apps.administracion.views.web.estado_web import estado_lista, estado_create, estado_editar, estado_eliminar
from apps.administracion.views.web.inicio_web import inicio
from apps.administracion.views.web.categoria_herramienta_web import categoria_lista, categoria_create, categoria_editar, categoria_eliminar
from apps.administracion.views.web.estado_herramienta_web import estado_herramienta_lista, estado_herramienta_create, estado_herramienta_editar, estado_herramienta_eliminar
from apps.administracion.views.web.herramienta_web import herramienta_lista, herramienta_create, herramienta_editar, herramienta_eliminar
from apps.administracion.views.web.inventario_herramienta_web import inventario_herramientas_lista, inventario_herramientas_create, inventario_herramientas_editar, inventario_herramientas_eliminar

router = DefaultRouter()

urlpatterns = [
    path('', inicio, name='inicio'),    
   
    
    path('clientes/', cliente_lista, name='clientes_lista'),
    path('clientes/crear/', cliente_create, name='clientes_crear'),
    path('clientes/editar/<int:cliente_id>/', cliente_editar, name='clientes_editar'),
    path('clientes/eliminar/<int:cliente_id>/', cliente_eliminar, name='clientes_eliminar'),
    path('clientes/<int:cliente_id>/detalle/', cliente_detalle_json, name='clientes_detalle_json'),
    
    path('marcas/', marca_lista, name='marcas_lista'),
    path('marcas/crear/', marca_create, name='marcas_crear'),
    path('marcas/editar/<int:marca_id>/', marca_editar, name='marcas_editar'),
    path('marcas/eliminar/<int:marca_id>/', marca_eliminar, name='marcas_eliminar'),
    
    path('combustibles/', combustible_lista, name='combustibles_lista'),
    path('combustibles/crear/', combustible_create, name='combustibles_crear'),
    path('combustibles/editar/<int:combustible_id>/', combustible_editar, name='combustibles_editar'),
    path('combustibles/eliminar/<int:combustible_id>/', combustible_eliminar, name='combustibles_eliminar'),
    
    path('modelos/', modelo_lista, name='modelos_lista'),
    path('modelos/crear/', modelo_create, name='modelo_crear'),
    path('modelos/editar/<int:modelo_id>/', modelo_editar, name='modelo_editar'),
    path('modelos/eliminar/<int:modelo_id>/', modelo_eliminar, name='modelo_eliminar'),
    
    path('vehiculos/', vehiculo_lista, name='vehiculos_lista'),
    path('vehiculos/crear/', vehiculo_create, name='vehiculo_crear'),
    path('vehiculos/editar/<int:vehiculo_id>/', vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', vehiculo_eliminar, name='vehiculo_eliminar'),

   
    path('recepciones/<int:recepcion_id>/evidencias/',evidencia_lista,name='evidencia_lista'),
    path('recepciones/<int:recepcion_id>/evidencias/crear/',evidencia_create,name='evidencia_create'),
    path('evidencias/<int:evidencia_id>/editar/',evidencia_editar,name='evidencia_editar'),
    path('evidencias/<int:evidencia_id>/eliminar/',evidencia_eliminar,name='evidencia_eliminar'),

    path('categorias/', categoria_lista, name='categorias_lista'),
    path('categorias/crear/', categoria_create, name='categorias_crear'),
    path('categorias/editar/<int:categoria_id>/', categoria_editar, name='categorias_editar'),
    path('categorias/eliminar/<int:categoria_id>/', categoria_eliminar, name='categorias_eliminar'),

    path('servicios/', servicio_lista, name='servicios_lista'),
    path('servicios/crear/', servicio_create, name='servicios_crear'),
    path('servicios/editar/<int:servicio_id>/', servicio_editar, name='servicios_editar'),
    path('servicios/eliminar/<int:servicio_id>/', servicio_eliminar,  name='servicios_eliminar'),

    


    path('estados/', estado_lista, name='estados_lista'),
    path('estados/crear/', estado_create, name='estados_crear'),
    path('estados/editar/<int:estado_id>/', estado_editar, name='estados_editar'),
    path('estados/eliminar/<int:estado_id>/', estado_eliminar, name='estados_eliminar'),



    path('categoria_herramientas/', categoria_lista, name='categoria_herramientas_lista'),
    path('categoria_herramientas/crear/', categoria_create, name='categoria_herramientas_crear'),
    path('categoria_herramientas/editar/<int:categoria_id>/', categoria_editar, name='categoria_herramientas_editar'),
    path('categoria_herramientas/eliminar/<int:categoria_id>/', categoria_eliminar, name='categoria_herramientas_eliminar'),  

    path('estado_herramientas/', estado_herramienta_lista, name='estado_herramientas_lista'),
    path('estado_herramientas/crear/', estado_herramienta_create, name='estado_herramientas_crear'),
    path('estado_herramientas/editar/<int:estado_id>/', estado_herramienta_editar, name='estado_herramientas_editar'),
    path('estado_herramientas/eliminar/<int:estado_id>/', estado_herramienta_eliminar, name='estado_herramientas_eliminar'),  

    path('herramientas/', herramienta_lista, name='herramientas_lista'),
    path('herramientas/crear/', herramienta_create, name='herramientas_crear'),
    path('herramientas/editar/<int:herramienta_id>/', herramienta_editar, name='herramientas_editar'),
    path('herramientas/eliminar/<int:herramienta_id>/', herramienta_eliminar, name='herramientas_eliminar'),

    path('inventario_herramientas/', inventario_herramientas_lista, name='inventario_herramientas_lista'),
    path('inventario_herramientas/crear/', inventario_herramientas_create, name='inventario_herramientas_crear'),
    path('inventario_herramientas/editar/<int:inventario_id>/', inventario_herramientas_editar, name='inventario_herramientas_editar'),
    path('inventario_herramientas/eliminar/<int:inventario_id>/', inventario_herramientas_eliminar, name='inventario_herramientas_eliminar'),


    
    
]
    
    

    
