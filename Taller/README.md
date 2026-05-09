Taller - Backend (Django)
=================================

Resumen rápido
- Proyecto Django que contiene la app `apps.administracion` y configuración en `config/`.
- Este README describe cómo preparar un entorno reproducible y ejecutar el proyecto en desarrollo.

Requisitos
- Python 3.10+ (recomendado)
- MySQL (o adaptar `DATABASES` en `config/settings.py`)

Pasos de instalación (Windows - PowerShell)

1. Crear y activar entorno virtual

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

2. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Variables y configuración
- Revisa `config/settings.py` para `DATABASES` y credenciales de Cloudinary; en producción usa variables de entorno.

4. Migraciones y seeds

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_roles
python manage.py seed_permisos
# ejecutar otros seeders en apps/administracion/management/commands
```

5. Ejecutar servidor en desarrollo

```powershell
python manage.py runserver
```

Notes sobre rutas y ejecución
- Las rutas HTTP están definidas en `config/urls.py` y mapean a vistas en `apps.administracion.views.*`.
- Ejecuta comandos administrados con `python manage.py <command>` (p. ej. `migrate`, `runserver`, seeders personalizados).
- `manage.py` requiere que el entorno tenga instaladas las dependencias (no hay activación automática desde el código).

Buenas prácticas recomendadas
- Añadir `.venv/` a `.gitignore` si no está.
- Añadir un `scripts/setup.ps1` y `scripts/setup.sh` para estandarizar el proceso de setup del equipo.
- Considerar `requirements-lock.txt` o `poetry` para reproducibilidad.
- Para despliegue/CI, usar `Dockerfile` o `devcontainer.json`.

¿Siguientes pasos sugeridos?
- Puedo crear los scripts `scripts/setup.ps1` y `scripts/setup.sh` automáticamente.
- Puedo añadir `.venv` a `.gitignore` y un corto `CONTRIBUTING.md` con normas de entorno.

Contacto
- Si quieres que añada scripts o cambie el README, dime qué prefieres.
