from django.core.management.base import BaseCommand
from django.db import transaction

from apps.administracion.models import CategoriaServicio


class Command(BaseCommand):
    help = "Crea categorías de servicio base en la base de datos"

    def handle(self, *args, **options):
        categorias = [
                
            {
                "nombre": "Mantenimiento Preventivo",
                "descripcion": "Servicios programados para prevenir fallas y mantener el vehículo en buen estado.",
                "is_active": True,
            },
            {
                "nombre": "Mecánica General",
                "descripcion": "Reparaciones generales del motor y componentes mecánicos.",
                "is_active": True,
            },
            {
                "nombre": "Sistema de Frenos",
                "descripcion": "Servicios relacionados con frenos y seguridad del vehículo.",
                "is_active": True,
            },
            {
                "nombre": "Suspensión y Dirección",
                "descripcion": "Servicios para mejorar estabilidad y control del vehículo.",
                "is_active": True,
            },
            {
                "nombre": "Sistema Eléctrico",
                "descripcion": "Diagnóstico y reparación de componentes eléctricos.",
                "is_active": True,
            },
            {
                "nombre": "Diagnóstico",
                "descripcion": "Identificación de fallas mediante revisión técnica o escáner.",
                "is_active": True,
            },
            {
                "nombre": "Aire Acondicionado",
                "descripcion": "Mantenimiento y reparación del sistema de climatización.",
                "is_active": True,
            },
            {
                "nombre": "Transmisión",
                "descripcion": "Servicios relacionados con cajas de cambio y embrague.",
                "is_active": True,
            },
            {
                "nombre": "Instalación de Accesorios",
                "descripcion": "Instalación de mejoras y accesorios para el vehículo.",
                "is_active": True,
            }


        ]

        creadas = 0
        existentes = 0

        with transaction.atomic():
            for data in categorias:
                _, created = CategoriaServicio.objects.get_or_create(
                    nombre=data["nombre"],
                    descripcion=data["descripcion"],
                    is_active=data["is_active"]
                )
                if created:
                    creadas += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de categorías de servicio completado. Creadas: {creadas}. Ya existentes: {existentes}."
            )     )