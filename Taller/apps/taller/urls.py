from django.urls import path

from .views.web.cliente_web import cliente_lista, cliente_create, cliente_editar, cliente_eliminar, cliente_detalle_json
from .views.web.evidencia_web import evidencia_lista,evidencia_create,evidencia_eliminar,evidencia_detalle,evidencia_editar
from .views.web.recepcion_web import recepcion_lista, recepcion_create, recepcion_detalle, recepcion_eliminar
from .views.web.orden_servicio_web import orden_lista, orden_detalle, orden_create, orden_editar, orden_cerrar, orden_eliminar
from .views.web.orden_servicio_detalle_web import detalle_create, detalle_editar, detalle_eliminar

urlpatterns = [
    path('clientes/', cliente_lista, name='clientes_lista'),
    path('clientes/crear/', cliente_create, name='cliente_crear'),
    path('clientes/<int:cliente_id>/editar/', cliente_editar, name='clientes_editar'),
    path('clientes/<int:cliente_id>/eliminar/', cliente_eliminar, name='clientes_eliminar'),
    path('clientes/<int:cliente_id>/detalle-json/', cliente_detalle_json, name='cliente_detalle_json'),

    path('recepciones/<int:recepcion_id>/evidencias/', evidencia_lista, name='evidencia_lista'),
    path('recepciones/<int:recepcion_id>/evidencias/crear/', evidencia_create, name='evidencia_crear'),
    path('evidencias/<int:evidencia_id>/editar/', evidencia_editar, name='evidencia_editar'),
    path('evidencias/<int:evidencia_id>/eliminar/', evidencia_eliminar, name='evidencia_eliminar'),
    path('evidencias/<int:evidencia_id>/detalle/', evidencia_detalle, name='evidencia_detalle'),

    path('recepciones/', recepcion_lista, name='recepciones_lista'),
    path('recepciones/crear/', recepcion_create, name='recepciones_crear'),
    path('recepciones/<int:recepcion_id>/detalle/', recepcion_detalle, name='recepcion_detalle'),
    path('recepciones/<int:recepcion_id>/eliminar/', recepcion_eliminar, name='recepcion_eliminar'),

    path('ordenes/', orden_lista, name='ordenes_lista'),
    path('ordenes/<int:orden_id>/detalle/', orden_detalle, name='orden_detalle'),
    path('ordenes/crear/', orden_create, name='ordenes_crear'),
    path('ordenes/<int:orden_id>/editar/', orden_editar, name='orden_editar'),
    path('ordenes/<int:orden_id>/cerrar/', orden_cerrar, name='orden_cerrar'),
    path('ordenes/<int:orden_id>/eliminar/', orden_eliminar, name='orden_eliminar'),

    path('ordenes/<int:orden_id>/detalle/crear/', detalle_create, name='detalle_crear'),
    path('ordenes/detalle/<int:detalle_id>/editar/', detalle_editar, name='detalle_editar'),
    path('ordenes/detalle/<int:detalle_id>/eliminar/', detalle_eliminar, name='detalle_eliminar'),

]

