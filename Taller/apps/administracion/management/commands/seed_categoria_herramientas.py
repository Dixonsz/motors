from django.core.management.base import BaseCommand
from django.db import transaction
from apps.administracion.models import CategoriaHerramienta


class Command(BaseCommand):
    help = "Crea categorías de herramientas base en la base de datos"

    def handle(self, *args, **options):
        categorias_herramientas = [
            {
                "nombre": "Herramientas manuales",
                "descripcion": "Herramientas operadas sin energía eléctrica o neumática, utilizadas para tareas básicas como ajuste, ensamblaje y desmontaje.",
            },
            {
                "nombre": "Herramientas eléctricas",
                "descripcion": "Herramientas alimentadas por electricidad, utilizadas para tareas que requieren mayor potencia o precisión.",
            },
            {
                "nombre": "Herramientas neumáticas",
                "descripcion": "Herramientas alimentadas por aire comprimido, utilizadas para tareas que requieren alta potencia o precisión.",
            },
            {
                "nombre": "Diagnóstico",
                "descripcion": "Herramientas utilizadas para diagnosticar problemas y medir parámetros técnicos.",
            },
            {
                "nombre": "Equipos de elevación",
                "descripcion": "Herramientas utilizadas para elevar y mover cargas pesadas.",
            },
            {
                "nombre": "Medición y calibración",
                "descripcion": "Herramientas utilizadas para medir y calibrar parámetros técnicos.",
            },
            {
                "nombre": "Soldadura y corte",
                "descripcion": "Herramientas utilizadas para realizar soldadura y corte de materiales.",
            },
            {
                "nombre": "Herramientas de mano especializadas",
                "descripcion": "Herramientas de mano diseñadas para tareas específicas y especializadas.",
            },
            {
                "nombre": "Equipos de seguridad",
                "descripcion": "Herramientas utilizadas para garantizar la seguridad de los trabajadores.",
            },
             {
                "nombre": "Herramientas de limpieza",
                "descripcion": "Herramientas utilizadas para limpiar y mantener el entorno de trabajo.",
            },



        ]

        creados = 0
        existentes = 0

        with transaction.atomic():
            for data in categorias_herramientas:
                _, created = CategoriaHerramienta.objects.get_or_create(
                    nombre=data["nombre"],
                    defaults={
                        "descripcion": data["descripcion"],
                    },
                )
                if created:
                    creados += 1
                else:
                    existentes += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de categorías de herramientas completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
