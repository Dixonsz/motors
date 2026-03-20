from django.core.management.base import BaseCommand
from django.db import transaction

from apps.administracion.models import Marca


class Command(BaseCommand):
    help = "Crea marcas base en la base de datos"

    def handle(self, *args, **options):
        marcas = [
                {
                    "nombre": "Toyota",
                },
                {
                    "nombre": "Honda",
                },
                {
                    "nombre": "Ford",
                },
                {
                    "nombre": "Chevrolet",
                },
                {
                    "nombre": "Nissan",
                },
                {
                    "nombre": "Volkswagen",
                },
                {
                    "nombre": "Hyundai",
                },
                {
                    "nombre": "Kia",
                },
                {
                    "nombre": "Mazda",
                },
                {
                    "nombre": "Subaru",
                },
                {
                    "nombre": "Mercedes-Benz",
                },
                {
                    "nombre": "BMW",
                },
                {
                    "nombre": "Audi",
                },
                {
                    "nombre": "Lexus",
                },
                {
                    "nombre": "Jeep",
                },
                {
                    "nombre": "Dodge",
                },
                {
                    "nombre": "Ram",
                },
                {
                    "nombre": "GMC",
                },
                {
                    "nombre": "Cadillac",
                },
                {
                    "nombre": "Buick",
                },
                {
                    "nombre": "Acura",
                },
                {
                    "nombre": "Infiniti",
                },
                {
                    "nombre": "Lincoln",
                },
                {
                    "nombre": "Volvo",
                },
                

        ]

        creadas = 0
        existentes = 0

        with transaction.atomic():
            for data in marcas:
                _, created = Marca.objects.get_or_create(
                    nombre=data["nombre"],
                )
                if created:
                    creadas += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de marcas completado. Creadas: {creadas}. Ya existentes: {existentes}."
            )     )