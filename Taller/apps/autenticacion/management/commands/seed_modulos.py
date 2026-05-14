from django.core.management.base import BaseCommand
from django.db import transaction

from apps.autenticacion.models.modulo import Modulo


class Command(BaseCommand):
    help = "Crea módulos base en la base de datos"

    def handle(self, *args, **options):
        modulos = [
            {
                "nombre": "Citas",
                "descripcion": "Acceso a la gestión de citas, incluyendo creación, edición y eliminación de citas para servicios automotrices.",
            },
            {
                "nombre": "Herramientas",
                "descripcion": "Acceso a la gestión de herramientas, incluyendo creación, edición y eliminación de herramientas utilizadas en el taller.",
            },
            {
                "nombre": "Servicios",
                "descripcion": "Acceso a la gestión de servicios, incluyendo creación, edición y eliminación de servicios ofrecidos por el taller.",
            },
            {
                "nombre": "Clientes",
                "descripcion": "Acceso a la gestión de clientes, incluyendo creación, edición y eliminación de información de clientes.",
            },
            {
                "nombre": "Vehiculos",
                "descripcion": "Acceso a la gestión de vehículos, incluyendo creación, edición y eliminación de información de vehículos.",
            },
            {
                "nombre": "Configuraciones",
                "descripcion": "Acceso a la gestión de configuraciones del sistema.",
            },
            {
                "nombre": "Estados",
                "descripcion": "Acceso a la gestión de estados de los vehículos.",
            },
            {
                "nombre": "Roles",
                "descripcion": "Acceso a la gestión de roles y permisos de los usuarios del sistema.",
            },
            {
                "nombre": "Recepciones",
                "descripcion": "Acceso a la gestión de recepciones, incluyendo creación, edición y eliminación de recepciones de vehículos para servicios.",
            },
            {
                "nombre": "Usuarios",
                "descripcion": "Acceso a la gestión de usuarios, incluyendo creación, edición y eliminación de información de usuarios.",
            },
             



        ]

        creadas = 0
        existentes = 0

        with transaction.atomic():
            for data in modulos:
                _, created = Modulo.objects.get_or_create(
                    nombre=data["nombre"],
                    descripcion=data["descripcion"]
                )
                if created:
                    creadas += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de módulos completado. Creadas: {creadas}. Ya existentes: {existentes}."
            )     )
