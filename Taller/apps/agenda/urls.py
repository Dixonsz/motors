from django.urls import path

from apps.agenda.views.web.calendario_web import calendario_view, citas_calendario, calendario_form_data, calendario_vehiculos_por_cliente
from apps.agenda.views.api.calendario_view import CalendarioApiView
from apps.agenda.views.web.cita_web import cita_lista, cita_create, cita_editar, cita_eliminar
from apps.agenda.views.web.configuracion_calendario_web import configuracion_lista, configuracion_create, configuracion_editar, configuracion_eliminar
from apps.agenda.views.web.servicio_web import servicio_lista, servicio_create, servicio_editar, servicio_eliminar
from apps.agenda.views.web.categoria_servicio_web import categoria_lista, categoria_create, categoria_editar, categoria_eliminar

urlpatterns = [
    path('calendario/', calendario_view, name='calendario_citas'),
    path('calendario/eventos/', citas_calendario, name='citas_calendario'),
    path('calendario/form-data/', calendario_form_data, name='calendario_form_data'),
    path('calendario/vehiculos-por-cliente/<int:cliente_id>/', calendario_vehiculos_por_cliente, name='calendario_vehiculos_por_cliente'),  
    path('calendario/crear/', CalendarioApiView().crear_cita, name='calendario_crear_cita'),
   
    path('citas/', cita_lista, name='citas_lista'),
    path('citas/crear/', cita_create, name='citas_crear'),
    path('citas/editar/<int:cita_id>/', cita_editar, name='citas_editar'),
    path('citas/eliminar/<int:cita_id>/', cita_eliminar, name='citas_eliminar'),

    path('calendario/configuraciones/', configuracion_lista, name='configuracion_lista'),
    path('calendario/configuraciones/crear/', configuracion_create, name='configuracion_crear'),
    path('calendario/configuraciones/editar/<int:configuracion_id>/', configuracion_editar, name='configuracion_editar'),
    path('calendario/configuraciones/eliminar/<int:configuracion_id>/', configuracion_eliminar, name='configuracion_eliminar'),

    path('servicios/', servicio_lista, name='servicios_lista'),
    path('servicios/crear/', servicio_create, name='servicios_crear'),
    path('servicios/editar/<int:servicio_id>/', servicio_editar, name='servicios_editar'),
    path('servicios/eliminar/<int:servicio_id>/', servicio_eliminar, name='servicios_eliminar'),

    path('categorias/', categoria_lista, name='categorias_lista'),
    path('categorias/crear/', categoria_create, name='categorias_crear'),
    path('categorias/editar/<int:categoria_id>/', categoria_editar, name='categorias_editar'),
    path('categorias/eliminar/<int:categoria_id>/', categoria_eliminar, name='categorias_eliminar'),
]