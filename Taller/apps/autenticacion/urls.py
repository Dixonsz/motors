from django.urls import path
from .views.web.auth_web import login_view, logout_view,recover_account_view, reset_password_view
from .views.web.modulo_web import modulo_crear, modulo_editar, modulo_eliminar, modulo_lista
from .views.web.permiso_web import permiso_lista, rol_permisos_lista, permiso_create, permiso_eliminar
from .views.web.rol_permiso_web import rol_permiso_lista, rol_permiso_asignar, rol_permiso_asignar_modulo, rol_permiso_revocar, rol_permiso_revocar_modulo
from .views.web.rol_web import rol_create, rol_editar, rol_eliminar, rol_lista
from .views.web.usuario_web import usuario_lista, usuario_create, usuario_editar, usuario_cambiar_password, usuario_activar_desactivar

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recover-account/', recover_account_view, name='recover_account'),
    path('reset-password/<str:token>/', reset_password_view, name='reset_password'),

    path('modulos/', modulo_lista, name='modulos_lista'),
    path('modulos/crear/', modulo_crear, name='modulos_crear'),
    path('modulos/editar/<int:modulo_id>/', modulo_editar, name='modulos_editar'),
    path('modulos/eliminar/<int:modulo_id>/', modulo_eliminar, name='modulos_eliminar'),

    path('permisos/', permiso_lista, name='permisos_lista'),
    path('roles/<int:rol_id>/permisos/', rol_permisos_lista, name='rol_permisos_lista'),
    path('permisos/crear/', permiso_create, name='permisos_crear'),
    path('permisos/eliminar/<int:permiso_id>/', permiso_eliminar, name='permisos_eliminar'),

    path('roles/<int:rol_id>/permisos/asignar/', rol_permiso_asignar, name='rol_permisos_asignar'),
    path('roles/<int:rol_id>/permisos/asignar-modulo/', rol_permiso_asignar_modulo, name='rol_permisos_asignar_modulo'),
    path('roles/<int:rol_id>/permisos/revocar/', rol_permiso_revocar, name='rol_permisos_revocar'),
    path('roles/<int:rol_id>/permisos/revocar-modulo/', rol_permiso_revocar_modulo, name='rol_permisos_revocar_modulo'),
    path('roles/<int:rol_id>/permisos/', rol_permiso_lista, name='rol_permisos_lista'),

    path('roles/', rol_lista, name='roles_lista'),
    path('roles/crear/', rol_create, name='roles_crear'),
    path('roles/editar/<int:rol_id>/', rol_editar, name='roles_editar'),
    path('roles/eliminar/<int:rol_id>/', rol_eliminar, name='roles_eliminar'),

    path('usuarios/', usuario_lista, name='usuarios_lista'),
    path('usuarios/crear/', usuario_create, name='usuarios_crear'),
    path('usuarios/editar/<int:usuario_id>/', usuario_editar, name='usuarios_editar'),
    path('usuarios/cambiar-password/<int:usuario_id>/', usuario_cambiar_password, name='usuarios_cambiar_password'),
    path('usuarios/activar-desactivar/<int:usuario_id>/', usuario_activar_desactivar, name='usuarios_activar_desactivar'),
]