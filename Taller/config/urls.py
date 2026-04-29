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
from apps.administracion.views.web.modulo_web import modulo_lista, modulo_crear, modulo_editar, modulo_eliminar
from apps.administracion.views.web.permiso_web import permiso_lista, permiso_create, permiso_eliminar, rol_permiso_lista
from apps.administracion.views.web.rol_web import rol_lista, rol_create, rol_editar, rol_eliminar
from apps.administracion.views.web.rol_permiso_web import rol_permiso_lista, rol_permiso_asignar, rol_permiso_asignar_modulo, rol_permiso_revocar
from apps.administracion.views.web.cita_web import cita_lista, cita_create, cita_editar, cita_eliminar
from apps.administracion.views.web.recepcion_web import recepcion_lista, recepcion_create, recepcion_detalle, recepcion_eliminar
from apps.administracion.views.web.orden_servicio_web import orden_lista, orden_create, orden_detalle, orden_editar, orden_cerrar, orden_eliminar
from apps.administracion.views.web.orden_servicio_detalle_web import detalle_create, detalle_editar, detalle_eliminar
from apps.administracion.views.web.usuario_web import usuario_lista, usuario_create, usuario_editar,usuario_cambiar_password,usuario_activar_desactivar
from apps.administracion.views.web.calendario_web import calendario_view, citas_calendario, calendario_form_data, calendario_vehiculos_por_cliente
from apps.administracion.views.web.configuracion_calendario_web import bloqueo_lista, bloqueo_create, bloqueo_editar, bloqueo_eliminar
from apps.administracion.views.api.calendario_view import CalendarioApiView

calendario_api = CalendarioApiView()

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

    path('modulos/', modulo_lista, name='modulos_lista'),
    path('modulos/crear/', modulo_crear, name='modulos_crear'),
    path('modulos/editar/<int:modulo_id>/', modulo_editar, name='modulo_editar'),
    path('modulos/eliminar/<int:modulo_id>/', modulo_eliminar, name='modulo_eliminar'),

    

    path('roles/', rol_lista, name='roles_lista'),
    path('roles/crear/', rol_create, name='roles_crear'),
    path('roles/editar/<int:rol_id>/', rol_editar, name='roles_editar'),
    path('roles/eliminar/<int:rol_id>/', rol_eliminar, name='roles_eliminar'),
    path('roles/', permiso_lista, name='permisos_lista'),
    path('roles/crear/', permiso_create, name='permisos_crear'),
    path('roles/eliminar/<int:permiso_id>/', permiso_eliminar, name='permisos_eliminar'),
    path('roles/<int:rol_id>/', rol_permiso_lista, name='rol_permiso_lista'),
    path('roles/<int:rol_id>/asignar/', rol_permiso_asignar, name='rol_permiso_asignar'),
    path('roles/<int:rol_id>/asignar_modulo/', rol_permiso_asignar_modulo, name='rol_permiso_asignar_modulo'),
    path('roles/<int:rol_id>/<int:permiso_id>/revocar/', rol_permiso_revocar, name='rol_permiso_revocar'),

    path('citas/calendario/',calendario_view,name='citas_calendario'),
    path('citas/calendario/json/',citas_calendario,name='citas_calendario_json'),
    path('citas/calendario/form-data/',calendario_form_data,name='calendario_form_data'),
    path('citas/calendario/vehiculos/<int:cliente_id>/',calendario_vehiculos_por_cliente,   name='calendario_vehiculos'),
    path('citas/calendario/crear/',calendario_api.crear_cita, name='calendario_crear_cita'),  

    path('citas/', cita_lista, name='citas_lista'),
    path('citas/crear/', cita_create, name='citas_crear'),
    path('citas/<int:cita_id>/editar/', cita_editar, name='citas_editar'),
    path('citas/<int:cita_id>/eliminar/', cita_eliminar, name='citas_eliminar'),

    path('recepciones/', recepcion_lista, name='recepciones_lista'),
    path('recepciones/crear/', recepcion_create, name='recepciones_crear'),
    path('recepciones/<int:recepcion_id>/', recepcion_detalle, name='recepciones_detalle'),
    path('recepciones/<int:recepcion_id>/eliminar/', recepcion_eliminar, name='recepciones_eliminar'),

    path('ordenes/', orden_lista, name='ordenes_lista'),
    path('ordenes/crear/', orden_create, name='ordenes_crear'),
    path('ordenes/<int:orden_id>/', orden_detalle, name='orden_detalle'),
    path('ordenes/<int:orden_id>/editar/', orden_editar, name='ordenes_editar'),
    path('ordenes/<int:orden_id>/cerrar/', orden_cerrar, name='ordenes_cerrar'),
    path('ordenes/<int:orden_id>/eliminar/', orden_eliminar, name='ordenes_eliminar'),

    path('ordenes/<int:orden_id>/servicios/agregar/', detalle_create, name='detalle_crear'),
    path('ordenes/servicios/<int:detalle_id>/editar/', detalle_editar, name='detalle_editar'),
    path('ordenes/servicios/<int:detalle_id>/eliminar/', detalle_eliminar, name='detalle_eliminar'),

    path('usuarios/', usuario_lista, name='usuarios_lista'),
    path('usuarios/crear/', usuario_create, name='usuarios_crear'),
    path('usuarios/editar/<int:usuario_id>/', usuario_editar, name='usuarios_editar'),
    path('usuarios/<int:usuario_id>/cambiar-password/', usuario_cambiar_password, name='usuarios_cambiar_password'),
    path('usuarios/<int:usuario_id>/activar-desactivar/', usuario_activar_desactivar, name='usuarios_activar_desactivar'),

    path('citas/bloqueos/',bloqueo_lista,    name='bloqueos_lista'),
    path('citas/bloqueos/crear/',bloqueo_create,   name='bloqueos_crear'),
    path('citas/bloqueos/<int:bloqueo_id>/editar/',bloqueo_editar,   name='bloqueos_editar'),
    path('citas/bloqueos/<int:bloqueo_id>/eliminar/',bloqueo_eliminar, name='bloqueos_eliminar'),

   


    
    
]
    
    

    
