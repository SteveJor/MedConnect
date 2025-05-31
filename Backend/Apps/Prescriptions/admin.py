from django.contrib import admin
from .models import Ordonnance, Prescription

@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    """
    Administration des ordonnances.
    """
    list_display = (
        'numero_ordonnance', 'libelle', 'consultation_patient_name',
        'consultation_doctor_name', 'date_emission', 'duree_traitement', 'last_update'
    )
    list_display_links = ('numero_ordonnance', 'libelle')
    list_filter = ('date_emission', 'consultation__medical_personnel__specialite')
    search_fields = (
        'numero_ordonnance', 'libelle', 'consultation__patient__nom',
        'consultation__patient__prenom', 'consultation__medical_personnel__user__email'
    )
    readonly_fields = ('date_emission', 'last_update', 'numero_ordonnance')
    fieldsets = (
        (None, {
            'fields': ('consultation', 'numero_ordonnance', 'libelle')
        }),
        ('Détails', {
            'fields': ('date_emission', 'duree_traitement')
        }),
        ('Historique', {
            'fields': ('last_update',)
        }),
    )
    # Permet d'ajouter des Prescriptions directement depuis l'interface d'édition de l'Ordonnance.
    inlines = [] # Sera géré par PrescriptionInline

    def consultation_patient_name(self, obj):
        if obj.consultation and obj.consultation.patient:
            return f"{obj.consultation.patient.prenom} {obj.consultation.patient.nom}"
        return "N/A"
    consultation_patient_name.short_description = 'Patient'
    consultation_patient_name.admin_order_field = 'consultation__patient__nom'

    def consultation_doctor_name(self, obj):
        if obj.consultation and obj.consultation.medical_personnel:
            return f"Dr. {obj.consultation.medical_personnel.user.get_full_name() or obj.consultation.medical_personnel.user.email}"
        return "N/A"
    consultation_doctor_name.short_description = 'Médecin'
    consultation_doctor_name.admin_order_field = 'consultation__medical_personnel__user__last_name'


class PrescriptionInline(admin.TabularInline):
    """
    Permet d'ajouter/modifier des prescriptions directement depuis l'ordonnance.
    """
    model = Prescription
    extra = 1 # Nombre de formulaires vides à afficher par défaut
    fields = ('libelle', 'dosage', 'frequence', 'periode_de_prise', 'notes')
    readonly_fields = ('numero_prescription', 'date_creation', 'last_update')


# Mettre à jour l'admin Ordonnance pour inclure PrescriptionInline
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """
    Administration des prescriptions individuelles.
    """
    list_display = (
        'numero_prescription', 'libelle', 'dosage', 'frequence',
        'ordonnance_numero', 'ordonnance_patient_name', 'last_update'
    )
    list_display_links = ('numero_prescription', 'libelle')
    list_filter = ('frequence', 'date_creation', 'last_update')
    search_fields = (
        'numero_prescription', 'libelle', 'ordonnance__numero_ordonnance',
        'ordonnance__consultation__patient__nom', 'ordonnance__consultation__patient__prenom'
    )
    readonly_fields = ('date_creation', 'last_update', 'numero_prescription')
    fieldsets = (
        (None, {
            'fields': ('ordonnance', 'numero_prescription')
        }),
        ('Détails de la Prescription', {
            'fields': ('libelle', 'dosage', 'frequence', 'periode_de_prise', 'notes')
        }),
        ('Historique', {
            'fields': ('date_creation', 'last_update')
        }),
    )

    def ordonnance_numero(self, obj):
        if obj.ordonnance:
            return obj.ordonnance.numero_ordonnance
        return "N/A"
    ordonnance_numero.short_description = "N° Ordonnance"
    ordonnance_numero.admin_order_field = 'ordonnance__numero_ordonnance'

    def ordonnance_patient_name(self, obj):
        if obj.ordonnance and obj.ordonnance.consultation and obj.ordonnance.consultation.patient:
            return f"{obj.ordonnance.consultation.patient.prenom} {obj.ordonnance.consultation.patient.nom}"
        return "N/A"
    ordonnance_patient_name.short_description = 'Patient'
    ordonnance_patient_name.admin_order_field = 'ordonnance__consultation__patient__nom'

# Mettre à jour l'admin Ordonnance pour inclure PrescriptionInline
admin.site.unregister(Ordonnance) # Désenregistrer si déjà enregistré sans inline
@admin.register(Ordonnance)
class OrdonnanceAdminWithInline(OrdonnanceAdmin): # Hérite de notre OrdonnanceAdmin pour garder ses configs
    inlines = [PrescriptionInline]