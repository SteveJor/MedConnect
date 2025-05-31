from django.db import models
from Patients.models import Patient # Importe le modèle Patient

class DossierMedical(models.Model):
    """
    Modèle représentant le dossier médical d'un patient.
    Un patient a un seul dossier médical (OneToOneField).
    """
    # Liaison One-to-One avec le modèle Patient.
    # related_name='dossier_medical' permet d'accéder au dossier depuis l'objet Patient.
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE, # Si le patient est supprimé, son dossier l'est aussi.
        related_name='dossier_medical',
        help_text="The patient associated with this medical record."
    )

    # Note: `id_patient` du diagramme est implicite via la relation `patient`.
    # `numero_dossier` pourrait être auto-généré ou un champ unique.
    numero_dossier = models.CharField(
        max_length=100,
        unique=True,
        blank=True, # Peut être auto-généré au moment de la création
        null=True,
        help_text="Unique identifier for the medical record."
    )

    date_derniere_consultation = models.DateField(
        blank=True,
        null=True,
        help_text="Date of the last consultation recorded in this file."
    )
    dernier_acces = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last access/update to this medical record."
    )
    pathologie_chronique = models.TextField(
        blank=True,
        null=True,
        help_text="Details of chronic pathologies (e.g., diabetes, hypertension)."
    )
    allergies = models.TextField(
        blank=True,
        null=True,
        help_text="Known allergies (medications, food, environmental)."
    )
    antecedents_medicaux = models.TextField(
        blank=True,
        null=True,
        help_text="Past medical history, surgeries, major illnesses."
    )
    vaccinations = models.TextField(
        blank=True,
        null=True,
        help_text="Record of vaccinations received."
    )
    # last_update est déjà couverte par `dernier_acces` si c'est pour toute modification.
    # Si `last_update` est la dernière MAJ d'une information spécifique, on la garde.
    # Pour l'instant, on se base sur `dernier_acces` pour l'update du dossier.

    def save(self, *args, **kwargs):
        """
        Override de la méthode save pour générer un numéro de dossier si non fourni.
        """
        if not self.numero_dossier:
            # Générer un numéro de dossier simple. Peut être plus complexe.
            self.numero_dossier = f"D-{self.patient.user.id}-{models.UUIDField().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Retourne une représentation en chaîne du dossier médical.
        """
        return f"Dossier Médical de {self.patient.nom} {self.patient.prenom} ({self.numero_dossier})"

    class Meta:
        """
        Métadonnées du modèle DossierMedical.
        """
        verbose_name = _("Dossier Médical")
        verbose_name_plural = _("Dossiers Médicaux")
        ordering = ['patient__nom', 'patient__prenom']