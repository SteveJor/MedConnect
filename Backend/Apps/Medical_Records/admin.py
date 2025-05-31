from django.contrib import admin
from .models import DossierMedical

@admin.register(DossierMedical)
class DossierMedicalAdmin(admin.ModelAdmin):
    """
    Personnalisation de l'administration du modèle DossierMedical.
    """
    list_display = (
        'numero_dossier', 'patient_full_name', 'patient_email',
        'date_derniere_consultation', 'dernier_acces'
    )
    list_display_links = ('numero_dossier',)
    list_filter = ('date_derniere_consultation', 'dernier_acces')
    search_fields = (
        'numero_dossier', 'patient__user__email', 'patient__nom',
        'patient__prenom', 'pathologie_chronique', 'allergies'
    )
    readonly_fields = ('dernier_acces', 'numero_dossier') # Numero de dossier auto-généré

    fieldsets = (
        (None, {
            'fields': ('patient', 'numero_dossier',)
        }),
        ('Informations Générales', {
            'fields': ('date_derniere_consultation', 'dernier_acces')
        }),
        ('Historique Médical', {
            'fields': ('pathologie_chronique', 'allergies', 'antecedents_medicaux', 'vaccinations')
        }),
    )

    def patient_full_name(self, obj):
        """
        Affiche le nom complet du patient lié.
        """
        return f"{obj.patient.prenom} {obj.patient.nom}"
    patient_full_name.short_description = 'Patient'
    patient_full_name.admin_order_field = 'patient__nom' # Permet de trier par nom de patient

    def patient_email(self, obj):
        """
        Affiche l'email de l'utilisateur lié au patient.
        """
        return obj.patient.user.email
    patient_email.short_description = 'Email Patient'
    patient_email.admin_order_field = 'patient__user__email'