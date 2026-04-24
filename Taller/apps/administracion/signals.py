from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.rol import Rol
from .services.rol_permiso_service import RolPermisoService


@receiver(post_save, sender=Rol)
def asignar_permisos_default(sender, instance, created, **kwargs):
    if created:
        RolPermisoService.asignar_permisos_default(instance, instance.nombre)