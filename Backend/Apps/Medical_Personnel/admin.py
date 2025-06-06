from django.contrib import admin
from .models import MedicalPersonnel

@admin.register(MedicalPersonnel)
class MedicalPersonnelAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'administration du modèle MedicalPersonnel.
    """
    list_display = (
        'get_user_email', 'specialite', 'numero_licence', 'annee_exercice',
        'telephone_pro', 'last_update'
    )
    list_display_links = ('get_user_email', 'specialite', 'numero_licence')
    list_filter = ('specialite', 'annee_exercice', 'date_creation', 'last_update')
    search_fields = (
        'comptePatientLie__compteUtilisateur__email', 'comptePatientLie__nom', 'comptePatientLie__prenom',
        'numero_licence', 'specialite', 'email_pro', 'telephone_pro'
    )
    readonly_fields = ('date_creation', 'last_update')
    fieldsets = (
        (None, {
            'fields': ('comptePatientLie',)
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

    def get_user_email(self, obj):
        """
        Affiche l'email de l'utilisateur lié au patient lié.
        """
        try:
            return obj.comptePatientLie.compteUtilisateur.email
        except AttributeError:
            return "-"
    get_user_email.short_description = 'Email utilisateur'
    get_user_email.admin_order_field = 'comptePatientLie__compteUtilisateur__email'
