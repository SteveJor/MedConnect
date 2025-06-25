from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from Apps.Patients.models import *
from Apps.Patients.serializer import *
import secrets
import logging

# Récupère le modèle utilisateur personnalisé défini dans settings.AUTH_USER_MODEL
CompteUtilisateur = get_user_model()

# Importe votre serializer pour CompteUtilisateur
# En supposant que votre serializer se trouve dans un fichier nommé 'serializer.py' dans la même application
from .serializer import CompteUtilisateurSerializer

logger = logging.getLogger(__name__)

# --- ViewSet pour CompteUtilisateur ---
class CompteUtilisateurViewSet(viewsets.ModelViewSet):
    """
    Point d'API qui permet de visualiser ou de modifier les utilisateurs.
    Seuls les utilisateurs authentifiés peuvent voir/modifier leur propre profil.
    Les administrateurs peuvent gérer tous les profils d'utilisateurs.
    """
    queryset = CompteUtilisateur.objects.all()
    serializer_class = CompteUtilisateurSerializer
    permission_classes = [IsAuthenticated] # Par défaut, nécessite une authentification

    def get_queryset(self):
        """
        Restreint facultativement les utilisateurs retournés à un utilisateur donné,
        en filtrant par un `pk` dans l'URL.
        """
        # Si l'utilisateur est un membre du staff ou un superutilisateur, il peut voir tous les comptes
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CompteUtilisateur.objects.all()
        # Sinon, un utilisateur normal ne peut voir que son propre compte
        return CompteUtilisateur.objects.filter(pk=self.request.user.pk)

    def perform_create(self, serializer):
        """
        Hache le mot de passe lors de la création d'un nouvel utilisateur.
        """
        password = serializer.validated_data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password) # Hache le mot de passe
            user.save()

    def perform_update(self, serializer):
        """
        Hache le mot de passe s'il est mis à jour.
        """
        password = serializer.validated_data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password) # Hache le mot de passe
            user.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            logger.error(f"Erreur de validation lors de la création de l'utilisateur : {e.detail}")
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur : {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # S'assure qu'un utilisateur ne peut mettre à jour que son propre profil, sauf s'il est staff/superutilisateur
        if not (self.request.user.is_staff or self.request.user.is_superuser or instance == self.request.user):
            return Response({"detail": "Vous n'avez pas la permission de modifier ce profil."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Erreur de validation lors de la mise à jour de l'utilisateur : {e.detail}")
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# --- Vue pour la connexion de l'utilisateur ---
class LoginView(APIView):
    """
    Point d'API pour la connexion de l'utilisateur.
    Authentifie l'utilisateur et génère un jeton.
    """
    permission_classes = [AllowAny] # Autorise l'accès non authentifié à ce point d'API

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password') # Utilisez 'password' comme nom de champ

        if not email or not password:
            return Response({'error': 'Email et mot de passe sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authentifie l'utilisateur en utilisant la fonction authenticate intégrée de Django
        user = authenticate(request, username=email, password=password)

        if user:
            # Génère un nouveau jeton sécurisé pour l'utilisateur
            token = secrets.token_hex(32)
            user.token = token # Assigne le jeton au champ 'token' de l'utilisateur
            user.last_login = timezone.now() # Utilise le champ last_login d'AbstractUser
            user.save()
            patient= Patient.objects.get(compteUtilisateur = user)
            print(patient)

            serializer = { 'infoUser':CompteUtilisateurSerializer(user).data, 'infoPatient':PatientSerializer(patient).data }

            return Response({'token': token, 'user': serializer}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email ou mot de passe incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)

# --- Vue pour la déconnexion de l'utilisateur ---
class LogoutView(APIView):
    """
    Point d'API pour la déconnexion de l'utilisateur.
    Invalide le jeton de l'utilisateur.
    """
    permission_classes = [IsAuthenticated] # Seuls les utilisateurs authentifiés peuvent se déconnecter

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user.token = None # Efface le jeton
            user.save()
            return Response({'message': 'Déconnexion réussie.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erreur lors de la déconnexion pour l'utilisateur {request.user.email} : {e}")
            return Response({'error': 'Une erreur est survenue lors de la déconnexion.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)