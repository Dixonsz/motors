from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seeders del módulo vehículos'

    def handle(self, *args, **kwargs):
        call_command('seed_combustibles')
        call_command('seed_estados')
        call_command('seed_marcas')
        call_command('seed_modelos')  