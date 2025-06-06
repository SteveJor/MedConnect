from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CompteUtilisateur(AbstractUser):
    """
    Modèle d'utilisateur personnalisé utilisant l'email comme identifiant principal.
    """
    email = models.EmailField(_('Adresse email'), unique=True, help_text=_("Requis. 255 caractères maximum."))
    token = models.CharField(max_length=64, blank=True, null=True)  # Token généré lors de la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # toujours requis pour createsuperuser

    is_staff = models.BooleanField(
        default=False,
        help_text=_('Peut accéder à l’interface d’administration.'),
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text=_('A tous les droits sans restriction.'),
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=_('Groupes auxquels appartient cet utilisateur.'),
        verbose_name=_('groupes'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text=_('Permissions spécifiques accordées à cet utilisateur.'),
        verbose_name=_('permissions'),
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')
