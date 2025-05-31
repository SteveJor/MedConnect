from django.db import models
from Users.models import User # Importe le modèle User personnalisé

class Patient(models.Model):
    """
    Modèle représentant un patient.
    Chaque patient est lié à un utilisateur unique via un OneToOneField.
    """
    # Liaison One-to-One avec le modèle User.
    # related_name='patient_profile' permet d'accéder au profil Patient depuis l'objet User (user.patient_profile).
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # Si l'utilisateur est supprimé, le profil patient l'est aussi.
        related_name='patient_profile',
        help_text="The user account associated with this patient profile."
    )

    nom = models.CharField(max_length=100, help_text=_("Patient's last name."))
    prenom = models.CharField(max_length=100, help_text=_("Patient's first name."))
    date_naissance = models.DateField(help_text=_("Patient's date of birth."))
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Patient's phone number."
    )
    pays_residence = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country of residence."
    )
    # Choices pour le sexe pour assurer la cohérence des données.
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sexe = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        help_text="Patient's biological sex."
    )
    langue_parlee = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Language primarily spoken by the patient."
    )
    ville = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City of residence."
    )
    quartier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Neighborhood or district of residence."
    )
    poids = models.FloatField(blank=True, null=True, help_text=_("Patient's weight in kilograms."))
    taille = models.FloatField(blank=True, null=True, help_text=_("Patient's height in meters."))
    maladie_courante = models.TextField(
        blank=True,
        null=True,
        help_text="Any current medical conditions or symptoms."
    )
    maladie_familiale = models.TextField(
        blank=True,
        null=True,
        help_text="Any family history of diseases or conditions."
    )
    # auto_now=True met à jour la date/heure à chaque sauvegarde de l'objet.
    last_update = models.DateTimeField(auto_now=True, help_text=_("Date and time of the last update to the patient's profile."))
    # auto_now_add=True définit la date/heure à la création de l'objet et ne la modifie plus.
    date_creation = models.DateTimeField(auto_now_add=True, help_text=_("Date and time the patient's profile was created."))

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du patient.
        """
        return f"{self.prenom} {self.nom} (User: {self.user.email})"

    class Meta:
        """
        Métadonnées du modèle Patient.
        """
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        # Ordering par défaut pour les listes de patients
        ordering = ['nom', 'prenom']