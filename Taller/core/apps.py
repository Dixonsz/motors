from django.apps import AppConfig
import threading

_seed_lock = threading.Lock()
_seed_done = False

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        global _seed_done
        with _seed_lock:
            if _seed_done:
                return
            try:
                from django.db import connection
                connection.ensure_connection()
                from django.core.management import call_command
                call_command('seed')
                _seed_done = True
            except Exception as e:
                print(f'Seeders no ejecutados: {e}')