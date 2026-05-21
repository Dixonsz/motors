from django.contrib import admin
from django.urls import path, include

from apps.autenticacion.views.web.index_web import inicio


urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('autenticacion/', include('apps.autenticacion.urls')),
    path('vehiculos/', include('apps.vehiculos.urls')),
    path('taller/', include('apps.taller.urls')),
    path('agenda/', include('apps.agenda.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('consulta/', include('apps.taller.urls_public')),
]

handler429 = 'apps.taller.views.public.historial_web.ratelimit_error'