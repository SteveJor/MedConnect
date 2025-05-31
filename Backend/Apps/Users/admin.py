from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'administration du modèle User.
    Permet de gérer l'email comme champ unique pour la connexion.
    """
    # Ajoute 'email' aux champs affichés dans la liste des utilisateurs
    list_display = UserAdmin.list_display + ('email',)
    # Ajoute 'email' aux champs de recherche
    search_fields = ('email', 'username', 'first_name', 'last_name')
    # Ajoute 'email' au filtre
    list_filter = UserAdmin.list_filter + ('email',)

    # Modifie les champs affichés dans le formulaire d'ajout et de modification
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('email',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email',)}),
    )

    # Assurez-vous que l'email est unique pour la validation dans l'admin
    # UserAdmin gère déjà l'unicité de USERNAME_FIELD, mais une double vérification est bonne.
    # Dans les formulaires d'administration, l'email sera maintenant le champ d'identification principal.

    # Pour gérer les groupes directement depuis le formulaire utilisateur dans l'admin,
    # les champs 'groups' et 'user_permissions' sont déjà inclus dans UserAdmin.
    # Vous n'avez pas besoin de les redéfinir à moins que vous souhaitiez changer leur affichage.