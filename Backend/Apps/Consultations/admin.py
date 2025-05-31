from django.contrib import admin
from .models import DemandeConsultation, Consultation

@admin.register(DemandeConsultation)
class DemandeConsultationAdmin(admin.ModelAdmin):
    """
    Administration des demandes de consultation.
    """
    list_display = (
        'numero_demande', 'patient_full_name', 'patient_email',
        'statut', 'date_demande', 'last_update'
    )
    list_display_links = ('numero_demande',)
    list_filter = ('statut', 'date_demande', 'last_update')
    search_fields = (
        'numero_demande', 'patient__user__email', 'patient__nom',
        'patient__prenom', 'motif'
    )
    readonly_fields = ('date_demande', 'last_update', 'numero_demande')
    fieldsets = (
        (None, {
            'fields': ('patient', 'numero_demande', 'motif')
        }),
        ('Statut et Historique', {
            'fields': ('statut', 'date_demande', 'last_update')
        }),
    )

    def patient_full_name(self, obj):
        return f"{obj.patient.prenom} {obj.patient.nom}"
    patient_full_name.short_description = 'Patient'
    patient_full_name.admin_order_field = 'patient__nom'

    def patient_email(self, obj):
        return obj.patient.user.email
    patient_email.short_description = 'Email Patient'
    patient_email.admin_order_field = 'patient__user__email'


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    """
    Administration des consultations réelles.
    """
    list_display = (
        'numero_consultation', 'patient_full_name', 'medical_personnel_name',
        'date_consultation', 'type_consultation', 'compte_rendu_preview'
    )
    list_display_links = ('numero_consultation',)
    list_filter = ('type_consultation', 'date_consultation', 'medical_personnel')
    search_fields = (
        'numero_consultation', 'patient__user__email', 'patient__nom',
        'patient__prenom', 'medical_personnel__user__email',
        'medical_personnel__specialite', 'compte_rendu', 'diagnostic'
    )
    readonly_fields = ('date_creation', 'last_update', 'numero_consultation')
    fieldsets = (
        (None, {
            'fields': ('patient', 'medical_personnel', 'dossier_medical', 'demande_consultation', 'numero_consultation')
        }),
        ('Détails de la Consultation', {
            'fields': ('date_consultation', 'heure_debut', 'heure_fin', 'type_consultation')
        }),
        ('Compte Rendu Médical', {
            'fields': ('diagnostic', 'compte_rendu')
        }),
        ('Historique', {
            'fields': ('date_creation', 'last_update')
        }),
    )

    def patient_full_name(self, obj):
        return f"{obj.patient.prenom} {obj.patient.nom}"
    patient_full_name.short_description = 'Patient'
    patient_full_name.admin_order_field = 'patient__nom'

    def medical_personnel_name(self, obj):
        if obj.medical_personnel:
            return f"Dr. {obj.medical_personnel.user.get_full_name() or obj.medical_personnel.user.email}"
        return "N/A"
    medical_personnel_name.short_description = 'Personnel Médical'
    medical_personnel_name.admin_order_field = 'medical_personnel__user__last_name'

    def compte_rendu_preview(self, obj):
        """Affiche un aperçu du compte rendu."""
        return (obj.compte_rendu[:50] + '...') if obj.compte_rendu and len(obj.compte_rendu) > 50 else (obj.compte_rendu or 'N/A')
    compte_rendu_preview.short_description = 'Compte Rendu'