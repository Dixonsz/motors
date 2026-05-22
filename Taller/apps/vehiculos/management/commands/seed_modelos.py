from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Modelo


class Command(BaseCommand):
    help = "Crea modelos base en la base de datos"

    def handle(self, *args, **options):
        modelos = [
        {
            "nombre": "Sedan",
        },
        {
            "nombre": "Hatchback",
        },
        {
            "nombre": "SUV",
        },
        {
            "nombre": "Pickup",
        },
        {
            "nombre": "Coupe",
        },
        {
            "nombre": "Crossover",
        },
        {
            "nombre": "Minivan",
        },
        {
            "nombre": "Van",
        },
        {
            "nombre": "Microbus",
        },
        {
            "nombre": "4x4",
        },
        {
            "nombre": "Todoterreno",
        },
        {
            "nombre": "Electrico",
        },
        {
            "nombre": "Hibrido",
        },
        {
            "nombre": "Diesel",
        },
    ]

        creadas = 0
        existentes = 0

        with transaction.atomic():
            for data in modelos:
                _, created = Modelo.objects.get_or_create(
                    nombre=data["nombre"],
                )
                if created:
                    creadas += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de modelos completado. Creadas: {creadas}. Ya existentes: {existentes}."
            )     )
