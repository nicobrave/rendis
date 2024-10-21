from django.contrib import admin
from .models import CustomUser, Proyecto
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Agregamos el campo de rol en el admin
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Proyecto)
