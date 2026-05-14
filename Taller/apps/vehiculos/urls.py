from django.urls import path

from .views.web.combustible_web import combustible_lista, combustible_create, combustible_editar, combustible_eliminar
from .views.web.estado_web import estado_lista, estado_create, estado_editar, estado_eliminar
from .views.web.marca_web import marca_lista, marca_create, marca_editar, marca_eliminar
from .views.web.modelo_web import modelo_lista, modelo_create, modelo_editar, modelo_eliminar
from .views.web.vehiculo_web import vehiculo_lista, vehiculo_create, vehiculo_editar, vehiculo_eliminar


urlpatterns = [
    path('vehiculos/', vehiculo_lista, name='vehiculos_lista'),
    path('vehiculos/crear/', vehiculo_create, name='vehiculos_crear'),
    path('vehiculos/editar/<int:vehiculo_id>/', vehiculo_editar, name='vehiculos_editar'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', vehiculo_eliminar, name='vehiculos_eliminar'),

    path('marcas/', marca_lista, name='marcas_lista'),
    path('marcas/crear/', marca_create, name='marcas_crear'),
    path('marcas/editar/<int:marca_id>/', marca_editar, name='marcas_editar'),
    path('marcas/eliminar/<int:marca_id>/', marca_eliminar, name='marcas_eliminar'),

    path('modelos/', modelo_lista, name='modelos_lista'),
    path('modelos/crear/', modelo_create, name='modelos_crear'),
    path('modelos/editar/<int:modelo_id>/', modelo_editar, name='modelos_editar'),
    path('modelos/eliminar/<int:modelo_id>/', modelo_eliminar, name='modelos_eliminar'),

    path('combustibles/', combustible_lista, name='combustibles_lista'),
    path('combustibles/crear/', combustible_create, name='combustibles_crear'),
    path('combustibles/editar/<int:combustible_id>/', combustible_editar, name='combustibles_editar'),
    path('combustibles/eliminar/<int:combustible_id>/', combustible_eliminar, name='combustibles_eliminar'),

    path('estados/', estado_lista, name='estados_lista'),
    path('estados/crear/', estado_create, name='estados_crear'),
    path('estados/editar/<int:estado_id>/', estado_editar, name='estados_editar'),
    path('estados/eliminar/<int:estado_id>/', estado_eliminar, name='estados_eliminar'),
]