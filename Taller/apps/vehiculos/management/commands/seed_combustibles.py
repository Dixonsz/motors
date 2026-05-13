from django.core.management.base import BaseCommand
from django.db import transaction

from apps.administracion.models import Combustible


class Command(BaseCommand):
    help = "Crea combustibles base en la base de datos"

    def handle(self, *args, **options):
        combustibles = [
            {
                "nombre": "Gasolina"
            },
            {
                "nombre": "Diésel"
            },
            {
                "nombre": "Gas Licuado de Petróleo (GLP)"
            },
            {
                "nombre": "Gas Natural Comprimido (GNC)"
            },
            {
                "nombre": "Híbrido"
            },
            {
                "nombre": "Eléctrico"
            },
            {
                "nombre": "Etanol"
            },
            {
                "nombre": "Biodiésel"
            },
            {
                "nombre": "Hidrógeno"
            },
            {
                "nombre": "Otros"
            }
        ]

        creados = 0
        existentes = 0

        with transaction.atomic():
            for data in combustibles:
                _, created = Combustible.objects.get_or_create(
                    nombre=data["nombre"],
                    )
                if created:
                    creados += 1
                else:
                    existentes += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeder de combustibles completado. Creados: {creados}. Ya existentes: {existentes}."
            )
        )
