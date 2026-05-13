from ..models.rol_permiso import RolPermiso
from ..models.rol import Rol
from ..models.permiso import Permiso
from .utils import get_required_instance


class RolPermisoService:

    @staticmethod
    def get_permisos_by_rol(rol_id):
        return RolPermiso.objects.filter(rol_id=rol_id).select_related('permiso__modulo')

    @staticmethod
    def asignar_permiso(rol_id, permiso_id):
        rol     = get_required_instance(Rol, rol_id, "Rol no encontrado.")
        permiso = get_required_instance(Permiso, permiso_id, "Permiso no encontrado.")

        if RolPermiso.objects.filter(rol=rol, permiso=permiso).exists():
            raise ValueError(f"El rol '{rol.nombre}' ya tiene asignado el permiso '{permiso}'.")

        rol_permiso = RolPermiso(rol=rol, permiso=permiso)
        rol_permiso.save()
        return rol_permiso

    @staticmethod
    def asignar_permisos_modulo_completo(rol_id, modulo_id):
        rol = get_required_instance(Rol, rol_id, "Rol no encontrado.")
        permisos = Permiso.objects.filter(modulo_id=modulo_id)

        if not permisos.exists():
            raise ValueError("El módulo no tiene permisos definidos.")

        asignados = []
        for permiso in permisos:
            rol_permiso, created = RolPermiso.objects.get_or_create(rol=rol, permiso=permiso)
            if created:
                asignados.append(rol_permiso)

        return asignados

    @staticmethod
    def revocar_permiso(rol_id, permiso_id):
        rol_permiso = RolPermiso.objects.filter(rol_id=rol_id, permiso_id=permiso_id).first()
        if not rol_permiso:
            raise ValueError("El rol no tiene ese permiso asignado.")
        rol_permiso.delete()

    @staticmethod
    def revocar_permisos_modulo_completo(rol_id, modulo_id):
        permisos = RolPermiso.objects.filter(
            rol_id=rol_id,
            permiso__modulo_id=modulo_id
        )
        if not permisos.exists():
            raise ValueError("El rol no tiene permisos asignados para ese módulo.")
        permisos.delete()

    @staticmethod
    def asignar_permisos_default(rol, nombre_rol):
        defaults = {
            'administrador': {
                'modulos': ['Citas', 'Recepciones', 'Ordenes', 'Clientes', 'Vehiculos', 'Usuarios', 'Roles'],
                'acciones': ['ver', 'crear', 'editar', 'eliminar']
            },
            'recepcionista': {
                'modulos': ['Citas', 'Recepciones', 'Clientes', 'Vehiculos'],
                'acciones': ['ver', 'crear', 'editar']
            },
            'mecanico': {
                'modulos': ['Ordenes', 'Recepciones'],
                'acciones': ['ver', 'editar']
            },
        }

        config = defaults.get(nombre_rol.lower())
        if not config:
            return

        permisos = Permiso.objects.filter(
            modulo__nombre__in=config['modulos'],
            accion__in=config['acciones']
        )
        for permiso in permisos:
            RolPermiso.objects.get_or_create(rol=rol, permiso=permiso)