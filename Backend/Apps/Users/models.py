from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé étendant AbstractUser de Django.
    Utilise 'email' comme identifiant unique pour la connexion.
    """
    email = models.EmailField(_('email address'), unique=True, help_text=_("Required. 255 characters or fewer."))

    # Vous pouvez ajouter d'autres champs communs à tous les utilisateurs ici si nécessaire
    # Par exemple, un champ pour stocker le rôle principal, bien que les groupes soient préférables.
    # role_display_name = models.CharField(max_length=50, blank=True, null=True, help_text=_("Display name for the user's primary role."))

    # Définit l'email comme champ d'identification pour la connexion.
    USERNAME_FIELD = 'email'
    # Liste des champs qui seront demandés lors de la création d'un superuser via la commande createsuperuser.
    # L'username de AbstractUser est par défaut requis, nous le gardons ici même si nous utilisons l'email pour USERNAME_FIELD.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'utilisateur, généralement l'email.
        """
        return self.email

    class Meta:
        """
        Métadonnées du modèle User.
        """
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        # Définition de permissions spécifiques au modèle User, si besoin,
        # en plus des permissions auto-générées (add, change, delete, view).
        # permissions = [
        #     ("can_manage_roles", "Can manage user roles and permissions"),
        # ]

# --- Note sur les Proxy Models ---
# Les Proxy Models (SuperAdmin, AdministrativePersonnel, MedicalPersonnel, Patient dans la discussion précédente)
# ne sont pas définis ici car:
# 1. Ils ne permettent pas d'ajouter de nouveaux champs, ce qui est nécessaire pour Patient et MedicalPersonnel.
# 2. Pour SuperAdmin et AdministrativePersonnel, la distinction est principalement une question de permissions
#    et de flag is_superuser/is_staff, qui est mieux gérée par les groupes Django et la logique d'assignation.
#    Il n'y a pas de données supplémentaires à stocker pour ces "rôles".