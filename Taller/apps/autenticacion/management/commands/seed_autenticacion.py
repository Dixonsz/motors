from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seeders del módulo autenticación'

    def handle(self, *args, **kwargs):
        call_command('seed_modulos')
        call_command('seed_permisos')  
        call_command('seed_roles')  
        call_command('seed_superusuario')  