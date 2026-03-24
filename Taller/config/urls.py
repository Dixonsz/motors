from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.administracion.views.api.orden_view import OrdenView
from apps.administracion.views.api.orden_servicio_view import OrdenServicioView
from apps.administracion.views.api.cita_view import CitaView
from apps.administracion.views.web.rol_web import rol_lista, rol_create, rol_editar, rol_eliminar
from apps.administracion.views.web.usuario_web import usuario_lista, usuario_create, usuario_editar, usuario_eliminar
from apps.administracion.views.web.cliente_web import cliente_lista, cliente_create, cliente_editar, cliente_eliminar
from apps.administracion.views.web.marca_web import marca_lista, marca_create, marca_editar, marca_eliminar
from apps.administracion.views.web.combustible_web import combustible_lista, combustible_create, combustible_editar, combustible_eliminar
from apps.administracion.views.web.modelo_web import modelo_lista, modelo_create, modelo_editar, modelo_eliminar
from apps.administracion.views.web.vehiculo_web import vehiculo_lista, vehiculo_create, vehiculo_editar,vehiculo_eliminar
from apps.administracion.views.web.recepcion_web import recepcion_lista,recepcion_create,recepciones_editar,recepcion_eliminar
from apps.administracion.views.web.evidencia_web import evidencia_lista, evidencia_create,evidencia_editar,evidencia_eliminar
from apps.administracion.views.web.categoria_servicio_web import categoria_lista, categoria_create, categoria_editar, categoria_eliminar
from apps.administracion.views.web.servicio_web import servicio_lista, servicio_create, servicio_editar, servicio_eliminar
from apps.administracion.views.web.cita_web import cita_lista, cita_create, cita_editar, cita_eliminar, calendario_citas_lista
from apps.administracion.views.web.orden_web import (orden_lista, orden_create, orden_editar, orden_eliminar, orden_detalle_agregar, orden_detalle_eliminar, orden_detalle_actualizar)
from apps.administracion.views.web.estado_web import estado_lista, estado_create, estado_editar, estado_eliminar
from apps.administracion.views.web.agenda_horario_web import agenda_horario_lista, agenda_horario_create, agenda_horario_editar, agenda_horario_eliminar
from apps.administracion.views.web.inicio_web import inicio

router = DefaultRouter()
router.register(r'ordenes', OrdenView, basename='api-ordenes')
router.register(r'ordenes-detalle', OrdenServicioView, basename='api-ordenes-detalle')
router.register(r'citas', CitaView, basename='api-citas')

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    path('roles/', rol_lista, name='roles_lista'),
    path('roles/crear/', rol_create, name='roles_crear'),
    path('roles/editar/<int:rol_id>/', rol_editar, name='roles_editar'),
    path('roles/eliminar/<int:rol_id>/', rol_eliminar, name='roles_eliminar'),
    
    path('usuarios/', usuario_lista, name='usuarios_lista'),
    path('usuarios/crear/', usuario_create, name='usuarios_crear'),
    path('usuarios/editar/<int:usuario_id>/', usuario_editar, name='usuarios_editar'),
    path('usuarios/eliminar/<int:usuario_id>/', usuario_eliminar, name='usuarios_eliminar'),
    
    path('clientes/', cliente_lista, name='clientes_lista'),
    path('clientes/crear/', cliente_create, name='clientes_crear'),
    path('clientes/editar/<int:cliente_id>/', cliente_editar, name='clientes_editar'),
    path('clientes/eliminar/<int:cliente_id>/', cliente_eliminar, name='clientes_eliminar'),
    
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

    path('recepciones/', recepcion_lista, name='recepcion_lista'),
    path('recepciones/crear/', recepcion_create, name='recepcion_create'),
    path('recepciones/editar/<int:recepcion_id>/', recepciones_editar, name='recepciones_editar'),
    path('recepciones/eliminar/<int:recepcion_id>/', recepcion_eliminar, name='recepcion_eliminar'),

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

    path('citas/', cita_lista, name='citas_lista'),
    path('citas/calendario/', calendario_citas_lista, name='citas_calendario'),
    path('citas/crear/', cita_create, name='citas_crear'),
    path('citas/editar/<int:cita_id>/', cita_editar, name='citas_editar'),
    path('citas/eliminar/<int:cita_id>/', cita_eliminar, name='citas_eliminar'),

    path('ordenes/', orden_lista, name='ordenes_lista'),
    path('ordenes/crear/', orden_create, name='ordenes_crear'),
    path('ordenes/editar/<int:orden_id>/', orden_editar, name='ordenes_editar'),
    path('ordenes/eliminar/<int:orden_id>/', orden_eliminar, name='ordenes_eliminar'),
    path('ordenes/<int:orden_id>/detalle/agregar/', orden_detalle_agregar, name='ordenes_detalle_agregar'),
    path('ordenes/<int:orden_id>/detalle/<int:detalle_id>/actualizar/', orden_detalle_actualizar, name='ordenes_detalle_actualizar'),
    path('ordenes/<int:orden_id>/detalle/<int:detalle_id>/eliminar/', orden_detalle_eliminar, name='ordenes_detalle_eliminar'),

    path('estados/', estado_lista, name='estados_lista'),
    path('estados/crear/', estado_create, name='estados_crear'),
    path('estados/editar/<int:estado_id>/', estado_editar, name='estados_editar'),
    path('estados/eliminar/<int:estado_id>/', estado_eliminar, name='estados_eliminar'),

    path('agenda-horarios/', agenda_horario_lista, name='agenda_horarios_lista'),
    path('agenda-horarios/crear/', agenda_horario_create, name='agenda_horarios_crear'),
    path('agenda-horarios/editar/<int:agenda_horario_id>/', agenda_horario_editar, name='agenda_horarios_editar'),
    path('agenda-horarios/eliminar/<int:agenda_horario_id>/', agenda_horario_eliminar, name='agenda_horarios_eliminar'),
    
    

    

]