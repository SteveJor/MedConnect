from django.db import models
from Users.models import User # Importe le modèle User personnalisé

class MedicalPersonnel(models.Model):
    """
    Modèle représentant un membre du personnel médical qualifié.
    Chaque membre est lié à un utilisateur unique via un OneToOneField.
    """
    # Liaison One-to-One avec le modèle User.
    # related_name='medical_personnel_profile' permet d'accéder au profil médical depuis l'objet User.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # Si l'utilisateur est supprimé, le profil médical l'est aussi.
        related_name='medical_personnel_profile',
        help_text="The user account associated with this medical personnel profile."
    )

    numero_licence = models.CharField(
        max_length=100,
        unique=True, # Le numéro de licence doit être unique.
        help_text="Official medical license number."
    )
    specialite = models.CharField(
        max_length=100,
        help_text="Medical specialty (e.g., General Practitioner, Cardiologist)."
    )
    axe = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Specific area of focus or sub-specialty if applicable."
    )
    lieu = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Primary workplace or affiliated institution."
    )
    annee_exercice = models.IntegerField(
        blank=True,
        null=True,
        help_text="Year of professional practice commencement."
    )
    # L'email pro peut être différent de l'email de User si nécessaire.
    email_pro = models.EmailField(
        blank=True,
        null=True,
        help_text="Professional email address (optional, can be different from user's main email)."
    )
    photo_profil = models.ImageField(
        upload_to='medical_personnel_photos/', # Dossier où les photos seront stockées
        blank=True,
        null=True,
        help_text="Profile photo of the medical personnel."
    )
    telephone_pro = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Professional phone number."
    )
    last_update = models.DateTimeField(
        auto_now=True,
        help_text="Date and time of the last update to the medical personnel's profile."
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the medical personnel's profile was created."
    )

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du personnel médical.
        """
        # Utilise le nom complet de l'utilisateur lié ou son email si le nom n'est pas défini
        return f"Dr. {self.specialite} - {self.user.get_full_name() or self.user.email}"

    class Meta:
        """
        Métadonnées du modèle MedicalPersonnel.
        """
        verbose_name = _("Personnel Médical")
        verbose_name_plural = _("Personnel Médical")
        ordering = ['specialite', 'user__last_name']