from django.urls import path
from .views.public.historial_web import (
    consulta_busqueda,
    consulta_historial_placa,
    consulta_historial_cedula,
    consulta_orden_detalle
)

urlpatterns = [
    path('', consulta_busqueda, name='consulta_busqueda'),
    path('orden/<int:orden_id>/', consulta_orden_detalle, name='consulta_orden_detalle'),
    path('placa/<str:placa>/', consulta_historial_placa, name='consulta_historial_placa'),
    path('cedula/<str:cedula>/', consulta_historial_cedula, name='consulta_historial_cedula'),
]