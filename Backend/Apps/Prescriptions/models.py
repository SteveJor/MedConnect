from django.db import models
from Consultations.models import Consultation # Importe le modèle Consultation

class Ordonnance(models.Model):
    """
    Modèle représentant une ordonnance médicale, issue d'une consultation.
    """
    # Liaison Many-to-One: une ordonnance est liée à une consultation.
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE, # Si la consultation est supprimée, l'ordonnance l'est aussi.
        related_name='ordonnances',
        help_text="The consultation during which this prescription was issued."
    )

    numero_ordonnance = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique identifier for the prescription."
    )
    libelle = models.CharField(
        max_length=255,
        help_text="General title or description of the prescription."
    )
    date_emission = models.DateField(
        auto_now_add=True, # Date de création de l'ordonnance.
        help_text="Date when the prescription was issued."
    )
    duree_traitement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Duration of the treatment (e.g., '7 jours', '1 mois')."
    )
    # Le médecin signataire est implicitement le medical_personnel de la consultation.
    # Pour le redondant `medecinSignataire` du diagramme, on peut l'obtenir via `consultation.medical_personnel`.
    # Si on voulait stocker un signataire différent, ce serait un ForeignKey vers MedicalPersonnel.
    # medecin_signataire_override = models.ForeignKey(
    #     MedicalPersonnel, on_delete=models.SET_NULL, null=True, blank=True,
    #     related_name='ordonnances_signees', help_text="Override signee if different from consultation's medical personnel."
    # )

    last_update = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update to the prescription record."
    )

    def save(self, *args, **kwargs):
        """
        Génère un numéro d'ordonnance si non fourni.
        """
        if not self.numero_ordonnance:
            self.numero_ordonnance = f"ORD-{models.UUIDField().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ordonnance {self.numero_ordonnance} pour {self.consultation.patient.nom}"

    class Meta:
        verbose_name = _("Ordonnance")
        verbose_name_plural = _("Ordonnances")
        ordering = ['-date_emission']


class Prescription(models.Model):
    """
    Modèle représentant une prescription individuelle de médicament au sein d'une ordonnance.
    """
    # Liaison Many-to-One: plusieurs prescriptions peuvent être dans une ordonnance.
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE, # Si l'ordonnance est supprimée, ses prescriptions le sont aussi.
        related_name='prescriptions',
        help_text="The main prescription containing this specific medication order."
    )

    numero_prescription = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique identifier for this specific medication prescription."
    )
    libelle = models.CharField(
        max_length=255,
        help_text="Name of the medication or treatment."
    )
    dosage = models.CharField(
        max_length=100,
        help_text="Dosage of the medication (e.g., '500mg', '2ml')."
    )
    frequence = models.CharField(
        max_length=100,
        help_text="Frequency of administration (e.g., '2 fois par jour', 'chaque matin')."
    )
    periode_de_prise = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Period or duration for taking the medication (e.g., 'avant les repas', 'au coucher')."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional notes or instructions for this prescription."
    )
    last_update = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update to this prescription."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time this prescription was created."
    )

    def save(self, *args, **kwargs):
        """
        Génère un numéro de prescription si non fourni.
        """
        if not self.numero_prescription:
            self.numero_prescription = f"PRES-{models.UUIDField().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prescription de {self.libelle} ({self.dosage}) pour ordonnance {self.ordonnance.numero_ordonnance}"

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")
        ordering = ['ordonnance__numero_ordonnance', 'libelle']