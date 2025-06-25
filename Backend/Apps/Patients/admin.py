from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'administration du modèle Patient.
    """
    # Champs affichés dans la liste des patients dans l'interface d'administration.
    list_display = (
        'get_user_email', 'nom', 'date_naissance', 'telephone',
        'sexe', 'last_update'
    )
    # Champs cliquables qui mènent à la page de détail du patient.
    list_display_links = ('get_user_email', 'nom')
    # Champs de filtrage disponibles.
    list_filter = ('sexe', 'pays_residence', 'date_creation', 'last_update')
    # Champs utilisés pour la recherche.
    search_fields = (
        'compteUtilisateur__email', 'nom', 'telephone',
        'maladie_courante', 'maladie_familiale'
    )
    # Champs en lecture seule dans le formulaire d'administration.
    readonly_fields = ('date_creation', 'last_update')
    # Organisation des champs dans le formulaire d’édition.
    fieldsets = (
        (None, {
            'fields': ('compteUtilisateur',)
        }),
        ('Informations Personnelles', {
            'fields': ('nom', 'date_naissance', 'sexe', 'langue_parlee')
        }),
        ('Coordonnées', {
            'fields': ('telephone', 'pays_residence', 'ville', 'quartier')
        }),
        ('Informations Médicales', {
            'fields': ('poids', 'taille', 'maladie_courante', 'maladie_familiale')
        }),
        ('Historique', {
            'fields': ('date_creation', 'last_update')
        }),
    )

    def get_user_email(self, obj):
        """
        Affiche l'email de l'utilisateur lié au patient.
        """
        return obj.compteUtilisateur.email if obj.compteUtilisateur else "-"
    get_user_email.short_description = 'Email Utilisateur'
    get_user_email.admin_order_field = 'compteUtilisateur__email'
