from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.autenticacion.urls')),
    path('', include('apps.vehiculos.urls')),
    path('', include('apps.taller.urls')),
    path('', include('apps.agenda.urls')),
    path('', include('apps.inventario.urls')),
]