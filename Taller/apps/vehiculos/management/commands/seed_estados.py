from django.core.management.base import BaseCommand
from django.db import transaction

from apps.administracion.models import Estado


class Command(BaseCommand):
    help = "Crea estados base en la base de datos"

    def handle(self, *args, **options):
        estados = [
            {
                "nombre": "Pendiente",
                "descripcion": "Estado inicial de una orden",
            },
            {
                "nombre": "En Progreso",
                "descripcion": "La orden está siendo atendida",
            },
            {
                "nombre": "Completada",
                "descripcion": "La orden ha sido finalizada",
            },
        ]

        creados = 0
        existentes = 0

        with transaction.atomic():
            for data in estados:
                _, created = Estado.objects.get_or_create(
                    nombre=data["nombre"],
                    defaults={
                        "descripcion": data["descripcion"],
                        "is_active": True,
                    },
                )
                if created:
                    creados += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de estados completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
