from django.core.management.base import BaseCommand
from django.db import transaction
from apps.administracion.models import EstadoHerramienta 


class Command(BaseCommand):
    help = "Crea estados de herramientas base en la base de datos"

    def handle(self, *args, **options):
        estados_herramientas = [
            {
                "nombre": "Disponible",
            },
            {
                "nombre": "En Uso",
            },
            {
                "nombre": "No disponible",
            },
            {
                "nombre": "En Mantenimiento",
            },
            {
                "nombre": "Dañada",
            },
            {
                "nombre": "En reparación",
            },
            {
                "nombre": "Fuera de servicio",
            },
            {
                "nombre": "En préstamo",
            },
            {
                "nombre": "Extraviada",
            },
             {
                "nombre": "Retirada",
            },



        ]

        creados = 0
        existentes = 0

        with transaction.atomic():
            for data in estados_herramientas:
                _, created = EstadoHerramienta.objects.get_or_create(
                    nombre=data["nombre"],
                    defaults={
                        "is_active": True,
                    },
                )
                if created:
                    creados += 1
                else:
                    existentes += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de estados de herramientas completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
