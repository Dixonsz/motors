from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.autenticacion.models import Rol
from apps.autenticacion.models.permiso import Permiso
from apps.autenticacion.models.rol_permiso import RolPermiso


class Command(BaseCommand):
    help = "Crea/actualiza un usuario admin con rol administrador y todos los permisos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="Reasigna la contrasena del usuario admin a la credencial por defecto",
        )

    def handle(self, *args, **options):
        credentials = getattr(settings, "DEFAULT_LOGIN_CREDENTIALS", {})
        username = credentials.get("username", "admin")
        password = credentials.get("password", "Admin123*")

        with transaction.atomic():
            rol_admin = self._get_or_create_admin_role()
            self._assign_all_permissions_to_role(rol_admin)
            user = self._get_or_create_admin_user(username, password, rol_admin, options.get("reset_password"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Usuario admin listo: {user.username} (rol: {rol_admin.nombre})"
            )
        )

    def _get_or_create_admin_role(self):
        rol_admin, _ = Rol.objects.get_or_create(
            nombre="Administrador",
            defaults={"descripcion": "Acceso completo al sistema"},
        )
        return rol_admin

    def _assign_all_permissions_to_role(self, rol_admin):
        permisos = list(Permiso.objects.all())
        if not permisos:
            self.stdout.write(
                self.style.WARNING(
                    "No hay permisos en la base de datos. Ejecuta primero los seeders de modulos y permisos."
                )
            )
            return

        existentes = set(
            RolPermiso.objects.filter(rol=rol_admin).values_list("permiso_id", flat=True)
        )
        nuevos = [
            RolPermiso(rol=rol_admin, permiso=permiso)
            for permiso in permisos
            if permiso.id not in existentes
        ]
        if nuevos:
            RolPermiso.objects.bulk_create(nuevos)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Permisos asignados al rol administrador: {len(nuevos)}"
                )
            )

    def _get_or_create_admin_user(self, username, password, rol_admin, reset_password):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "nombre": "Admin",
                "apellido": "Sistema",
                "cedula": f"{username}-seed",
                "telefono": "0000000000",
                "direccion": "N/A",
                "rol": rol_admin,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
        else:
            updates = []
            if user.rol_id != rol_admin.id:
                user.rol = rol_admin
                updates.append("rol")
            if not user.is_staff:
                user.is_staff = True
                updates.append("is_staff")
            if not user.is_superuser:
                user.is_superuser = True
                updates.append("is_superuser")
            if not user.is_active:
                user.is_active = True
                updates.append("is_active")
            if reset_password:
                user.set_password(password)
                updates.append("password")
            if updates:
                user.save(update_fields=updates)

        return user
