from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seeders del módulo taller'

    def handle(self, *args, **kwargs):
        # No seeders defined for this module yet.
        self.stdout.write('  seed_taller sin seeders para ejecutar')