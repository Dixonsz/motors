from django.core.management.base import BaseCommand
from django.db import transaction

from apps.administracion.models import Rol


class Command(BaseCommand):
    help = "Crea roles base en la base de datos"

    def handle(self, *args, **options):
        roles = [
            {
                "nombre": "Administrador",
                "descripcion": "Acceso completo al sistema",
            },
            {
                "nombre": "Asesor",
                "descripcion": "Gestiona clientes, recepciones y ordenes",
            },
            {
                "nombre": "Tecnico",
                "descripcion": "Ejecuta diagnosticos y servicios",
            },
        ]

        creados = 0
        existentes = 0

        with transaction.atomic():
            for data in roles:
                _, created = Rol.objects.get_or_create(
                    nombre=data["nombre"],
                    defaults={"descripcion": data["descripcion"]},
                )
                if created:
                    creados += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de roles completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
