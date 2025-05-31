from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'administration du modèle Patient.
    """
    # Champs affichés dans la liste des patients dans l'interface d'administration.
    list_display = (
        'user_email', 'nom', 'prenom', 'date_naissance', 'telephone',
        'sexe', 'last_update'
    )
    # Champs cliquables qui mènent à la page de détail du patient.
    list_display_links = ('user_email', 'nom', 'prenom')
    # Champs par lesquels il est possible de filtrer la liste des patients.
    list_filter = ('sexe', 'pays_residence', 'date_creation', 'last_update')
    # Champs par lesquels il est possible de rechercher un patient.
    search_fields = (
        'user__email', 'nom', 'prenom', 'telephone',
        'maladie_courante', 'maladie_familiale'
    )
    # Champs à ne pas modifier dans le formulaire d'administration.
    readonly_fields = ('date_creation', 'last_update')
    # Organisation des champs dans le formulaire de détail/modification.
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Informations Personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'sexe', 'langue_parlee')
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

    def user_email(self, obj):
        """
        Méthode pour afficher l'email de l'utilisateur lié dans la liste_display.
        """
        return obj.user.email
    user_email.short_description = 'Email Utilisateur' # Nom de la colonne dans l'admin
    user_email.admin_order_field = 'user__email' # Permet de trier par email de l'utilisateur