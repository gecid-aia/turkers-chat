from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario

class UsuarioAdmin():
    model = Usuario


admin.site.register(Usuario, UsuarioAdmin)