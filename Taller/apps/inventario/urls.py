from django.urls import path
from views.web.categoria_herramienta_web import categoria_lista,categoria_create, categoria_editar, categoria_eliminar
from views.web.estado_herramienta_web import estado_herramienta_lista, estado_herramienta_create, estado_herramienta_editar, estado_herramienta_eliminar
from views.web.herramienta_web import herramienta_lista, herramienta_create, herramienta_editar, herramienta_eliminar
from views.web.inventario_herramienta_web import inventario_herramientas_lista, inventario_herramientas_create, inventario_herramientas_editar, inventario_herramientas_eliminar

patherns = [
    path('categorias/', categoria_lista, name='categorias_lista'),
    path('categorias/crear/', categoria_create, name='categorias_crear'),
    path('categorias/editar/<int:categoria_id>/', categoria_editar, name='categorias_editar'),
    path('categorias/eliminar/<int:categoria_id>/', categoria_eliminar, name='categorias_eliminar'),

    path('estados/', estado_herramienta_lista, name='estado_herramientas_lista'),
    path('estados/crear/', estado_herramienta_create, name='estado_herramientas_crear'),
    path('estados/editar/<int:estado_id>/', estado_herramienta_editar, name='estado_herramientas_editar'),
    path('estados/eliminar/<int:estado_id>/', estado_herramienta_eliminar, name='estado_herramientas_eliminar'),

    path('herramientas/', herramienta_lista, name='herramientas_lista'),
    path('herramientas/crear/', herramienta_create, name='herramientas_crear'),
    path('herramientas/editar/<int:herramienta_id>/', herramienta_editar, name='herramientas_editar'),
    path('herramientas/eliminar/<int:herramienta_id>/', herramienta_eliminar, name='herramientas_eliminar'),

    path('inventario/', inventario_herramientas_lista, name='inventario_herramientas_lista'),
    path('inventario/crear/', inventario_herramientas_create, name='inventario_herramientas_crear'),
    path('inventario/editar/<int:inventario_id>/', inventario_herramientas_editar, name='inventario_herramientas_editar'),
    path('inventario/eliminar/<int:inventario_id>/', inventario_herramientas_eliminar, name='inventario_herramientas_eliminar'),








]

