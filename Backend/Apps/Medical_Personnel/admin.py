from django.contrib import admin
from .models import MedicalPersonnel

@admin.register(MedicalPersonnel)
class MedicalPersonnelAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'administration du modèle MedicalPersonnel.
    """
    list_display = (
        'user_email', 'specialite', 'numero_licence', 'annee_exercice',
        'telephone_pro', 'last_update'
    )
    list_display_links = ('user_email', 'specialite', 'numero_licence')
    list_filter = ('specialite', 'annee_exercice', 'date_creation', 'last_update')
    search_fields = (
        'user__email', 'user__first_name', 'user__last_name',
        'numero_licence', 'specialite', 'email_pro', 'telephone_pro'
    )
    readonly_fields = ('date_creation', 'last_update')
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Informations Professionnelles', {
            'fields': (
                'numero_licence', 'specialite', 'axe', 'lieu',
                'annee_exercice', 'email_pro', 'telephone_pro', 'photo_profil'
            )
        }),
        ('Historique', {
            'fields': ('date_creation', 'last_update')
        }),
    )

    def user_email(self, obj):
        """
        Méthode pour afficher l'email de l'utilisateur lié dans la liste_display.
        """
        return obj.user.email
    user_email.short_description = 'Email Utilisateur'
    user_email.admin_order_field = 'user__email'