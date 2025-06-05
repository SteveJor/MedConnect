from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CompteUtilisateur

@admin.register(CompteUtilisateur)
class UserAdmin(BaseUserAdmin):
    model = CompteUtilisateur
    ordering = ['email']
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    search_fields = ('email', 'username', )
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (_('Informations de connexion'), {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('username', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (_('Créer un nouvel utilisateur'), {
            'classes': ('wide',),
            'fields': ('email', 'username',  'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
        }),
    )
