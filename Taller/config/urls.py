from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacion/', include('apps.autenticacion.urls')),
    path('vehiculos/', include('apps.vehiculos.urls')),
    path('taller/', include('apps.taller.urls')),
    path('agenda/', include('apps.agenda.urls')),
    path('inventario/', include('apps.inventario.urls')),
]