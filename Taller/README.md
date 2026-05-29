# Taller - Backend (Django)

Sistema de gestión para talleres automotrices desarrollado en Django. Incluye módulos para agenda, autenticación, inventario, servicios, vehículos y administración general. Estructurado para facilitar mantenimiento, escalabilidad y despliegue en entornos productivos.

---

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación Local](#instalación-local)
- [Seeders y Datos Iniciales](#seeders-y-datos-iniciales)
- [Despliegue en Railway](#despliegue-en-railway)
- [Variables de Entorno](#variables-de-entorno)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contribución](#contribución)

---

## Estructura del Proyecto

```
taller/
├── config/              # Configuración global (settings, urls, wsgi, middlewares)
├── apps/
│   ├── agenda/          # Módulo de agenda y citas
│   ├── autenticacion/   # Autenticación y gestión de usuarios
│   ├── inventario/      # Control de inventario
│   ├── taller/          # Servicios y gestión del taller
│   └── vehiculos/       # Registro de vehículos
├── templates/           # Plantillas base globales
├── static/              # Archivos estáticos globales
├── manage.py
├── requirements.txt
├── Procfile             # Comando de inicio para Railway
└── railway.json         # Configuración de despliegue
```

> Consulta `arbol_proyecto.md` para un desglose detallado de carpetas y archivos.

---

## Requisitos

- Python 3.10 o superior
- MySQL 8.0 o superior
- Redis
- Entorno virtual recomendado

---

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd taller
```

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DJANGO_SECRET_KEY=tu_secret_key
DJANGO_DEBUG=True
DJANGO_SECURITY_ACTIVE=False
DISABLE_ACCESS_SECURITY=True

DB_NAME=taller
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306

REDIS_URL=redis://127.0.0.1:6379/1

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

TURNSTILE_SITE_KEY=1x00000000000000000000AA
TURNSTILE_SECRET_KEY=1x0000000000000000000000000000000AA
TURNSTILE_VERIFY_URL=https://challenges.cloudflare.com/turnstile/v0/siteverify

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

> ⚠️ Nunca subas el archivo `.env` al repositorio. Asegúrate de que esté en `.gitignore`.

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

---

## Seeders y Datos Iniciales

Ejecuta los siguientes comandos para cargar datos base después de migrar:

```bash
python manage.py createsuperuser
python manage.py seed_roles
python manage.py seed_permisos
```

> Revisa otros seeders disponibles en `apps/*/management/commands/`.

---

## Despliegue en Railway

El proyecto está configurado para desplegarse en [Railway](https://railway.app).

### Servicios necesarios

Agrega los siguientes plugins desde el panel de Railway:

- **MySQL** → base de datos principal
- **Redis** → caché y rate limiting

### Variables de entorno en Railway

Configura las variables en la pestaña **Variables** de tu servicio. Las variables de los plugins se referencian directamente:

```env
DJANGO_SECRET_KEY=tu_secret_key_segura
DJANGO_DEBUG=False
DJANGO_SECURITY_ACTIVE=True
ALLOWED_HOSTS=tuapp.railway.app

# Base de datos — referencia automática del plugin MySQL
DB_NAME=$MYSQLDATABASE
DB_USER=$MYSQLUSER
DB_PASSWORD=$MYSQLPASSWORD
DB_HOST=$MYSQLHOST
DB_PORT=$MYSQLPORT

# Redis — referencia automática del plugin Redis
REDIS_URL=$REDIS_URL

CORS_ALLOWED_ORIGINS=https://tu-frontend.com
CSRF_TRUSTED_ORIGINS=https://tu-frontend.com
```

### Primer despliegue

Después del primer deploy, ejecuta desde **Run Command** en el panel de Railway:

```bash
python manage.py migrate
python manage.py seed_roles
python manage.py seed_permisos
python manage.py createsuperuser
```

---

## Variables de Entorno

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django |
| `DJANGO_DEBUG` | Modo debug (`True` / `False`) |
| `DJANGO_SECURITY_ACTIVE` | Activa configuraciones de seguridad adicionales |
| `DISABLE_ACCESS_SECURITY` | Desactiva controles de acceso (solo desarrollo) |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por coma |
| `DB_NAME` | Nombre de la base de datos |
| `DB_USER` | Usuario de la base de datos |
| `DB_PASSWORD` | Contraseña de la base de datos |
| `DB_HOST` | Host de la base de datos |
| `DB_PORT` | Puerto de la base de datos |
| `REDIS_URL` | URL de conexión a Redis |
| `CLOUDINARY_CLOUD_NAME` | Cloud name de Cloudinary |
| `CLOUDINARY_API_KEY` | API key de Cloudinary |
| `CLOUDINARY_API_SECRET` | API secret de Cloudinary |
| `EMAIL_BACKEND` | Backend de email |
| `EMAIL_HOST` | Servidor SMTP |
| `EMAIL_PORT` | Puerto SMTP |
| `EMAIL_USE_TLS` | Usar TLS (`True` / `False`) |
| `EMAIL_HOST_USER` | Usuario del email |
| `EMAIL_HOST_PASSWORD` | Contraseña del email |
| `DEFAULT_FROM_EMAIL` | Email remitente por defecto |
| `TURNSTILE_SITE_KEY` | Site key de Cloudflare Turnstile |
| `TURNSTILE_SECRET_KEY` | Secret key de Cloudflare Turnstile |
| `TURNSTILE_VERIFY_URL` | URL de verificación de Turnstile |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS (separados por coma) |
| `CSRF_TRUSTED_ORIGINS` | Orígenes de confianza para CSRF (separados por coma) |

---

## Tecnologías Utilizadas

- [Django](https://www.djangoproject.com/) — Framework web
- [Django REST Framework](https://www.django-rest-framework.org/) — API REST
- [MySQL](https://www.mysql.com/) — Base de datos
- [Redis](https://redis.io/) — Caché y rate limiting
- [Cloudinary](https://cloudinary.com/) — Almacenamiento de imágenes
- [Gunicorn](https://gunicorn.org/) — Servidor WSGI para producción
- [WhiteNoise](https://whitenoise.readthedocs.io/) — Archivos estáticos en producción
- [django-axes](https://django-axes.readthedocs.io/) — Protección contra fuerza bruta
- [Cloudflare Turnstile](https://www.cloudflare.com/products/turnstile/) — Protección CAPTCHA

---

## Contribución

1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Haz push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

Se recomienda seguir las normas de estilo de Django y Python (PEP 8).