from django.core.management.base import BaseCommand
from django.db import transaction

from apps.autenticacion.models.modulo import Modulo
from apps.autenticacion.models.permiso import Permiso


class Command(BaseCommand):
    help = "Crea permisos base para todos los módulos en la base de datos"

    def handle(self, *args, **options):
        acciones = ['ver', 'crear', 'editar', 'eliminar']

        modulos = Modulo.objects.all()

        if not modulos.exists():
            self.stdout.write(self.style.WARNING(
                "No hay módulos en la base de datos. Ejecutá primero el seeder de módulos."
            ))
            return

        creados = 0
        existentes = 0

        with transaction.atomic():
            for modulo in modulos:
                for accion in acciones:
                    _, created = Permiso.objects.get_or_create(
                        modulo=modulo,
                        accion=accion,
                    )
                    if created:
                        creados += 1
                        self.stdout.write(f"  ✅ {modulo.nombre} - {accion}")
                    else:
                        existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de permisos completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
