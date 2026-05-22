from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Ejecuta todos los seeders del sistema'

    def handle(self, *args, **kwargs):
        seeders = [
            'seed_agenda',
            'seed_autenticacion',
            'seed_inventario',
            'seed_taller',
            'seed_vehiculos',
        ]

        for seeder in seeders:
            self.stdout.write(f'  → Ejecutando {seeder}...')
            call_command(seeder)
            self.stdout.write(self.style.SUCCESS(f'  {seeder} completado'))

        self.stdout.write(self.style.SUCCESS('Todos los seeders ejecutados'))