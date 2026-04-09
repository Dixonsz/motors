import unicodedata


class AccessControlService:
    PERMISSION_OPTIONS = [
        {'key': 'acceso_dashboard', 'label': 'Dashboard', 'description': 'Puede entrar al panel principal.'},
        {'key': 'acceso_flujo', 'label': 'Flujo unificado', 'description': 'Puede crear recepcion y orden desde flujo guiado.'},
        {'key': 'acceso_citas', 'label': 'Citas', 'description': 'Puede gestionar citas y calendario.'},
        {'key': 'acceso_recepciones', 'label': 'Recepciones', 'description': 'Puede gestionar recepciones y evidencias.'},
        {'key': 'acceso_ordenes', 'label': 'Ordenes', 'description': 'Puede gestionar ordenes y detalles.'},
        {'key': 'acceso_catalogo', 'label': 'Catalogo', 'description': 'Puede gestionar clientes, vehiculos y servicios.'},
        {'key': 'acceso_usuarios', 'label': 'Usuarios', 'description': 'Puede gestionar usuarios del sistema.'},
        {'key': 'acceso_roles', 'label': 'Roles', 'description': 'Puede gestionar perfiles y permisos por rol.'},
        {'key': 'acceso_reportes', 'label': 'Reportes', 'description': 'Puede visualizar reportes.'},
        {'key': 'acceso_inventario', 'label': 'Inventario herramientas', 'description': 'Puede gestionar inventario de herramientas.'},
    ]

    @staticmethod
    def _permission_keys():
        return [item['key'] for item in AccessControlService.PERMISSION_OPTIONS]

    @staticmethod
    def _empty_permissions():
        return {key: False for key in AccessControlService._permission_keys()}

    @staticmethod
    def _all_permissions():
        return {key: True for key in AccessControlService._permission_keys()}

    @staticmethod
    def _normalize_text(value):
        if not value:
            return ''

        decomposed = unicodedata.normalize('NFD', str(value).strip().lower())
        return ''.join(char for char in decomposed if unicodedata.category(char) != 'Mn')

    @staticmethod
    def default_permissions_by_role(role_name):
        normalized_name = AccessControlService._normalize_text(role_name)
        permissions = AccessControlService._empty_permissions()
        permissions['acceso_dashboard'] = True

        if normalized_name in ('administrador', 'admin', 'superadmin', 'propietario'):
            return AccessControlService._all_permissions()

        if normalized_name in ('recepcionista', 'asesor'):
            permissions.update({
                'acceso_flujo': True,
                'acceso_citas': True,
                'acceso_recepciones': True,
                'acceso_ordenes': True,
                'acceso_catalogo': True,
                'acceso_reportes': True,
            })
            return permissions

        if normalized_name == 'mecanico':
            permissions.update({
                'acceso_citas': True,
                'acceso_recepciones': True,
                'acceso_ordenes': True,
            })
            return permissions

        if normalized_name in ('inventario', 'bodega'):
            permissions.update({
                'acceso_inventario': True,
            })
            return permissions

        return permissions

    @staticmethod
    def normalize_permissions(permissions):
        normalized = AccessControlService._empty_permissions()

        if isinstance(permissions, dict):
            for key in normalized.keys():
                if key in permissions:
                    normalized[key] = bool(permissions.get(key))

        return normalized

    @staticmethod
    def get_role_permissions(rol):
        if not rol:
            return AccessControlService._empty_permissions()

        defaults = AccessControlService.default_permissions_by_role(getattr(rol, 'nombre', ''))
        configured = AccessControlService.normalize_permissions(getattr(rol, 'permissions', {}))

        merged = defaults.copy()
        merged.update(configured)
        return merged

    @staticmethod
    def get_effective_permissions(usuario):
        if not usuario or not getattr(usuario, 'is_authenticated', False):
            return AccessControlService._empty_permissions()

        if getattr(usuario, 'is_superuser', False):
            return AccessControlService._all_permissions()

        rol_permissions = AccessControlService.get_role_permissions(getattr(usuario, 'rol', None))
        extra_permissions = AccessControlService.normalize_permissions(getattr(usuario, 'extra_permissions', {}))

        merged = rol_permissions.copy()
        for key, value in extra_permissions.items():
            if value:
                merged[key] = True

        return merged

    @staticmethod
    def has_permission(usuario, permission_key):
        if permission_key not in AccessControlService._permission_keys():
            return False

        permissions = AccessControlService.get_effective_permissions(usuario)
        return bool(permissions.get(permission_key, False))
