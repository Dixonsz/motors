import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        username = os.environ.get('MAINT_USER')
        password = os.environ.get('MAINT_PASSWORD')
        email = os.environ.get('MAINT_EMAIL', 'mantenimiento@example.com')
        cedula=os.environ.get('MAINT_CEDULA', '155813277909'),


        if not username or not password:
            self.stderr.write('Define MAINT_USER y MAINT_PASSWORD como variables de entorno')
            return

        if Usuario.objects.filter(username=username).exists():
            self.stdout.write('El usuario ya existe')
            return

        Usuario.objects.create_superuser(
            username=username,
            password=password,
            nombre='Dixon',
            apellido='Sanchez Soza',
            email=email,
            cedula=cedula,
            telefono='88940261',
            direccion='Guapiles, Pococí, Limón',
            rol=None,
        )
        self.stdout.write(self.style.SUCCESS('Usuario de mantenimiento creado'))