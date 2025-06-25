from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Patient
from .serializer import PatientSerializer, PatientSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from Apps.Users.models import CompteUtilisateur
from Apps.Users.serializer import CompteUtilisateurSerializer
import logging
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print("Erreurs de validation :", e.detail)
            return Response({
                "message": "Échec de la validation.",
                "erreurs": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Erreur inattendue :", str(e))
            return Response({
                "message": "Une erreur inattendue s'est produite.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- views.py (dans Apps/Patients/views.py)

logger = logging.getLogger(__name__)

class RegisterPatientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.get("user")
        patient_data = request.data.get("patient")

        if not user_data or not patient_data:
            return Response({"error": "Les données 'user' ou 'patient' sont manquantes."}, status=400)

        try:
            user_data["password"] = make_password(user_data["password"])
            user_data["is_staff"] = False
            user_data["is_superuser"] = False

            user_serializer = CompteUtilisateurSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            patient_data["compteUtilisateur"] = user.id
            patient_serializer = PatientSerializer(data=patient_data)
            patient_serializer.is_valid(raise_exception=True)
            patient_serializer.save()

            return Response({
                "message": "Inscription réussie.",
                "user": user_serializer.data,
                "patient": patient_serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Log détaillé des erreurs de validation côté serveur
            logger.error("Validation errors: %s", e.detail)

            # Retourner dans la réponse la structure complète des erreurs pour debug frontend
            return Response({
                "message": "Échec de la validation des données.",
                "erreurs": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("Unexpected error during registration: %s", str(e))
            return Response({"error": "Erreur serveur inattendue."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)