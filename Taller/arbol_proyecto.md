taller/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── middleware.py
│   └── security.py
├── templates/
│   ├── base.html
│   └── confirmar_eliminacion.html
├── static/
│   └── (assets globales)
└── apps/
    ├── __init__.py
    │
    ├── autenticacion/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── signals.py
    │   ├── urls.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── usuario.py
    │   │   ├── rol.py
    │   │   ├── permiso.py
    │   │   ├── rol_permiso.py
    │   │   └── modulo.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── auth_service.py
    │   │   ├── usuario_service.py
    │   │   ├── rol_service.py
    │   │   ├── permiso_service.py
    │   │   ├── modulo_service.py
    │   │   └── rol_permiso_service.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── auth_serializers.py
    │   │   ├── usuario_serializers.py
    │   │   ├── usuario_create_serializers.py
    │   │   ├── rol_serializers.py
    │   │   ├── permiso_serializers.py
    │   │   ├── modulo_serializers.py
    │   │   └── rol_permiso_serializers.py
    │   ├── views/
    │   │   ├── web/
    │   │   │   ├── auth_web.py
    │   │   │   ├── usuario_web.py
    │   │   │   ├── rol_web.py
    │   │   │   ├── permiso_web.py
    │   │   │   ├── modulo_web.py
    │   │   │   └── rol_permiso_web.py
    │   │   └── api/
    │   │       ├── auth_view.py
    │   │       ├── usuario_view.py
    │   │       ├── rol_view.py
    │   │       ├── permiso_view.py
    │   │       ├── modulo_view.py
    │   │       └── rol_permiso_view.py
    │   ├── templates/
    │   │   ├── auth/
    │   │   │   ├── login.html
    │   │   │   ├── recover_account.html
    │   │   │   └── reset_password.html
    │   │   ├── usuarios/
    │   │   │   ├── usuarios_lista.html
    │   │   │   ├── usuarios_crear.html
    │   │   │   ├── usuarios_editar.html
    │   │   │   └── usuarios_cambiar_password.html
    │   │   ├── roles/
    │   │   │   ├── roles_lista.html
    │   │   │   ├── roles_crear.html
    │   │   │   ├── roles_editar.html
    │   │   │   └── roles_eliminar.html
    │   │   ├── rol_permisos/
    │   │   │   ├── rol_permiso_lista.html
    │   │   │   ├── rol_permiso_asignar.html
    │   │   │   └── rol_permiso_asignar_modulo.html
    │   │   └── modulos/
    │   │       ├── modulos_lista.html
    │   │       ├── modulos_crear.html
    │   │       └── modulos_editar.html
    │   └── management/
    │       ├── __init__.py
    │       └── commands/
    │           ├── __init__.py
    │           ├── seed_roles.py
    │           ├── seed_permisos.py
    │           └── seed_modulos.py
    │
    ├── vehiculos/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── urls.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── vehiculo.py
    │   │   ├── marca.py
    │   │   ├── modelo.py
    │   │   ├── combustible.py
    │   │   └── estado.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── vehiculo_service.py
    │   │   ├── marca_service.py
    │   │   ├── modelo_service.py
    │   │   ├── combustible_service.py
    │   │   └── estado_service.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── vehiculo_serializers.py
    │   │   ├── marca_serializers.py
    │   │   ├── modelo_serializers.py
    │   │   ├── combustible_serializers.py
    │   │   └── estado_serializers.py
    │   ├── views/
    │   │   ├── web/
    │   │   │   ├── vehiculo_web.py
    │   │   │   ├── marca_web.py
    │   │   │   ├── modelo_web.py
    │   │   │   ├── combustible_web.py
    │   │   │   └── estado_web.py
    │   │   └── api/
    │   │       ├── vehiculo_view.py
    │   │       ├── marca_view.py
    │   │       ├── modelo_view.py
    │   │       ├── combustible_view.py
    │   │       └── estado_view.py
    │   ├── templates/
    │   │   ├── vehiculos/
    │   │   │   ├── vehiculos_lista.html
    │   │   │   ├── vehiculos_crear.html
    │   │   │   └── vehiculos_editar.html
    │   │   ├── marcas/
    │   │   │   ├── marcas_lista.html
    │   │   │   ├── marcas_crear.html
    │   │   │   └── marcas_editar.html
    │   │   ├── modelos/
    │   │   │   ├── modelos_lista.html
    │   │   │   ├── modelos_crear.html
    │   │   │   └── modelos_editar.html
    │   │   ├── combustibles/
    │   │   │   ├── combustibles_lista.html
    │   │   │   ├── combustibles_crear.html
    │   │   │   └── combustibles_editar.html
    │   │   └── estados/
    │   │       ├── estados_lista.html
    │   │       ├── estados_crear.html
    │   │       └── estados_editar.html
    │   └── management/
    │       ├── __init__.py
    │       └── commands/
    │           ├── __init__.py
    │           ├── seed_marcas.py
    │           ├── seed_combustibles.py
    │           └── seed_estados.py
    │
    ├── taller/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── urls.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── cliente.py
    │   │   ├── recepcion.py
    │   │   ├── orden_servicio.py
    │   │   ├── orden_servicio_detalle.py
    │   │   └── evidencia.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── cliente_service.py
    │   │   ├── recepcion_service.py
    │   │   ├── orden_servicio_service.py
    │   │   ├── orden_servicio_detalle_service.py
    │   │   └── evidencia_service.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── cliente_serializers.py
    │   │   ├── recepcion_serializers.py
    │   │   ├── orden_servicio_serializers.py
    │   │   ├── orden_servicio_detalle_serializers.py
    │   │   ├── orden_servicio_and_detalle_serializers.py
    │   │   └── evidencia_serializers.py
    │   ├── views/
    │   │   ├── web/
    │   │   │   ├── cliente_web.py
    │   │   │   ├── recepcion_web.py
    │   │   │   ├── orden_servicio_web.py
    │   │   │   ├── orden_servicio_detalle_web.py
    │   │   │   └── evidencia_web.py
    │   │   └── api/
    │   │       ├── cliente_view.py
    │   │       ├── recepcion_view.py
    │   │       ├── orden_servicio_view.py
    │   │       ├── orden_servicio_detalle_view.py
    │   │       └── evidencia_view.py
    │   ├── templates/
    │   │   ├── clientes/
    │   │   │   ├── clientes_lista.html
    │   │   │   ├── clientes_crear.html
    │   │   │   └── clientes_editar.html
    │   │   ├── recepciones/
    │   │   │   ├── recepciones_lista.html
    │   │   │   ├── recepciones_detalle.html
    │   │   │   └── recepciones_crear.html
    │   │   ├── ordenes/
    │   │   │   ├── ordenes_lista.html
    │   │   │   ├── ordenes_detalle.html
    │   │   │   ├── ordenes_crear.html
    │   │   │   ├── ordenes_editar.html
    │   │   │   ├── ordenes_cerrar.html
    │   │   │   ├── detalle_crear.html
    │   │   │   ├── detalle_editar.html
    │   │   │   └── detalle_eliminar.html
    │   │   └── evidencias/
    │   │       ├── evidencias_lista.html
    │   │       ├── evidencias_crear.html
    │   │       └── evidencias_editar.html
    │   └── management/
    │       ├── __init__.py
    │       └── commands/
    │           ├── __init__.py
    │           └── seed_estados.py
    │
    ├── agenda/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── urls.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── cita.py
    │   │   ├── servicio.py
    │   │   ├── categoria_servicio.py
    │   │   └── configuracion_calendario.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── cita_service.py
    │   │   ├── servicio_service.py
    │   │   ├── categoria_servicio_service.py
    │   │   ├── calendario_cita_service.py
    │   │   └── configuracion_calendario_service.py
    │   ├── serializers/
    │   │   ├── __init__.py
    │   │   ├── cita_serializers.py
    │   │   ├── servicio_serializers.py
    │   │   ├── categoria_servicio_serializers.py
    │   │   ├── calendario_serializers.py
    │   │   └── configuracion_calendario_serializers.py
    │   ├── views/
    │   │   ├── web/
    │   │   │   ├── cita_web.py
    │   │   │   ├── servicio_web.py
    │   │   │   ├── categoria_servicio_web.py
    │   │   │   ├── calendario_web.py
    │   │   │   └── configuracion_calendario_web.py
    │   │   └── api/
    │   │       ├── cita_view.py
    │   │       ├── servicio_view.py
    │   │       ├── categoria_servicio_view.py
    │   │       ├── calendario_view.py
    │   │       └── configuracion_calendario_view.py
    │   ├── templates/
    │   │   ├── citas/
    │   │   │   ├── citas_lista.html
    │   │   │   ├── citas_crear.html
    │   │   │   └── citas_editar.html
    │   │   ├── servicios/
    │   │   │   ├── servicios_lista.html
    │   │   │   ├── servicios_crear.html
    │   │   │   └── servicios_editar.html
    │   │   ├── categoria_servicios/
    │   │   │   ├── categoria_servicios_lista.html
    │   │   │   ├── categoria_servicios_crear.html
    │   │   │   ├── categoria_servicios_editar.html
    │   │   │   └── categoria_servicios_eliminar.html
    │   │   └── calendario/
    │   │       ├── citas_calendario.html
    │   │       └── configuracion/
    │   │           ├── configuracion_lista.html
    │   │           └── configuracion_form.html
    │   ├── static/
    │   │   ├── js/
    │   │   │   ├── calendario.js
    │   │   │   └── configuracion_form.js
    │   │   └── css/
    │   │       └── calendario.css
    │   └── management/
    │       ├── __init__.py
    │       └── commands/
    │           ├── __init__.py
    │           └── seed_categoria_servicios.py
    │
    └── inventario/
        ├── __init__.py
        ├── apps.py
        ├── urls.py
        ├── models/
        │   ├── __init__.py
        │   ├── herramienta.py
        │   ├── categoria_herramienta.py
        │   ├── estado_herramienta.py
        │   └── inventario_herramienta.py
        ├── services/
        │   ├── __init__.py
        │   ├── herramienta_service.py
        │   ├── categoria_herramienta_service.py
        │   ├── estado_herramienta_service.py
        │   └── inventario_herramienta_service.py
        ├── serializers/
        │   ├── __init__.py
        │   ├── herramienta_serializers.py
        │   ├── categoria_herramienta_serializers.py
        │   ├── estado_herramienta_serializers.py
        │   └── inventario_herramienta_serializers.py
        ├── views/
        │   ├── web/
        │   │   ├── herramienta_web.py
        │   │   ├── categoria_herramienta_web.py
        │   │   ├── estado_herramienta_web.py
        │   │   └── inventario_herramienta_web.py
        │   └── api/
        │       ├── herramienta_view.py
        │       ├── categoria_herramienta_view.py
        │       ├── estado_herramienta_view.py
        │       └── inventario_herramienta_view.py
        ├── templates/
        │   ├── herramientas/
        │   │   ├── herramientas_lista.html
        │   │   ├── herramientas_crear.html
        │   │   └── herramientas_editar.html
        │   ├── categoria_herramienta/
        │   │   ├── categoria_herramientas_lista.html
        │   │   ├── categoria_herramientas_crear.html
        │   │   ├── categoria_herramientas_editar.html
        │   │   └── categoria_herramientas_eliminar.html
        │   ├── estado_herramientas/
        │   │   ├── estado_herramientas_lista.html
        │   │   ├── estado_herramientas_crear.html
        │   │   └── estado_herramientas_editar.html
        │   └── inventario_herramientas/
        │       ├── inventario_herramientas_lista.html
        │       ├── inventario_herramientas_crear.html
        │       └── inventario_herramientas_editar.html
        └── management/
            ├── __init__.py
            └── commands/
                ├── __init__.py
                ├── seed_categoria_herramientas.py
                └── seed_estado_herramientas.py