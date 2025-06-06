from django.db import models
from Apps.Patients.models import Patient
from Apps.Medical_Personnel.models import MedicalPersonnel
from django.utils.translation import gettext_lazy as _
from Apps.Medical_Records.models import DossierMedical # Pour lier aux dossiers médicaux

class DemandeConsultation(models.Model):
    """
    Modèle représentant une demande de consultation faite par un patient.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE, # Si le patient est supprimé, ses demandes le sont aussi.
        related_name='demandes_consultation',
        help_text="The patient who initiated this consultation request."
    )
    # Liaison Many-to-One: une consultation est effectuée par un personnel médical.
    medical_personnel = models.ForeignKey(
        MedicalPersonnel,
        on_delete=models.SET_NULL, # Si le personnel médical est supprimé, les consultations restent.
        null=True,
        blank=True,
        related_name='reception_demandes_consultation_medecin',
        help_text="The medical personnel who conducted the consultation."
    )
    # L'ID de la consultation peut être généré à la création ou lié à la consultation effective
    # Gardons-le comme un champ unique pour la demande si une consultation n'est pas encore créée.
    # `numero_consultation` du diagramme semble être une référence à la consultation future.
    # Ici, c'est l'ID de la demande.
    numero_demande = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique identifier for the consultation request."
    )

    # Statut de la demande (En attente, Acceptée, Refusée, Annulée)
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ACCEPTED', 'Acceptée'),
        ('REJECTED', 'Refusée'),
        ('CANCELLED', 'Annulée'),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current status of the consultation request."
    )
    motif = models.TextField(
        help_text="Reason for the consultation request."
    )
    date_demande = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the consultation request was made."
    )
    last_update = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update to the request status."
    )

    def save(self, *args, **kwargs):
        """
        Génère un numéro de demande si non fourni.
        """
        if not self.numero_demande:
            self.numero_demande = f"REQ-{models.UUIDField().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Demande {self.numero_demande} par {self.patient.nom} ({self.statut})"

    class Meta:
        verbose_name = _("Demande de Consultation")
        verbose_name_plural = _("Demandes de Consultations")
        ordering = ['-date_demande']


class Consultation(models.Model):
    """
    Modèle représentant une consultation médicale réalisée.
    """
    # Liaison Many-to-One: une consultation est faite pour un patient.
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consultations',
        help_text="The patient who received the consultation."
    )
    # Liaison Many-to-One: une consultation est effectuée par un personnel médical.
    medical_personnel = models.ForeignKey(
        MedicalPersonnel,
        on_delete=models.SET_NULL, # Si le personnel médical est supprimé, les consultations restent.
        null=True,
        blank=True,
        related_name='consultations_effectuees',
        help_text="The medical personnel who conducted the consultation."
    )
    # Liaison One-to-One (optionnelle) à une demande de consultation.
    # Une consultation peut résulter d'une demande, mais pas toujours.
    demande_consultation = models.OneToOneField(
        DemandeConsultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation_reelle',
        help_text="The original consultation request, if any."
    )
    # Liaison Many-to-One avec le Dossier Médical (pour la relation "être lié à").
    dossier_medical = models.ForeignKey(
        DossierMedical,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultations_liees',
        help_text="The medical record associated with this consultation."
    )

    numero_consultation = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique identifier for the consultation."
    )
    date_consultation = models.DateField(
        help_text="Date when the consultation took place."
    )
    heure_debut = models.TimeField(
        help_text="Start time of the consultation."
    )
    heure_fin = models.TimeField(
        blank=True,
        null=True,
        help_text="End time of the consultation."
    )
    TYPE_CHOICES = [
        ('ONLINE', 'En ligne'),
        ('IN_PERSON', 'En personne'),
    ]
    type_consultation = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='ONLINE',
        help_text="Type of consultation (online or in-person)."
    )
    compte_rendu = models.TextField(
        blank=True,
        null=True,
        help_text="Medical report or summary of the consultation."
    )
    diagnostic = models.TextField(
        blank=True,
        null=True,
        help_text="Diagnosis made during the consultation."
    )
    last_update = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update to the consultation record."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the consultation record was created."
    )

    def save(self, *args, **kwargs):
        """
        Génère un numéro de consultation si non fourni et met à jour le dossier médical.
        """
        if not self.numero_consultation:
            self.numero_consultation = f"CONSULT-{models.UUIDField().hex[:8]}"

        # Mettre à jour la date_derniere_consultation dans le DossierMedical
        if self.patient and self.dossier_medical:
            if not self.dossier_medical.date_derniere_consultation or \
               self.date_consultation > self.dossier_medical.date_derniere_consultation:
                self.dossier_medical.date_derniere_consultation = self.date_consultation
                self.dossier_medical.save(update_fields=['date_derniere_consultation'])

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Consultation {self.numero_consultation} avec Dr. {self.medical_personnel} pour {self.patient}"

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")
        ordering = ['-date_consultation', '-heure_debut']