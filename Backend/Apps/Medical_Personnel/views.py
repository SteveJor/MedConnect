from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import MedicalPersonnel
from .serializer import MedicalPersonnelSerializer
import os

class MedicalPersonnelViewSet(viewsets.ModelViewSet):
    queryset = MedicalPersonnel.objects.all()
    serializer_class = MedicalPersonnelSerializer

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

        # Supprime l'ancienne photo si une nouvelle est uploadée
        if 'photo_profil' in request.data and instance.photo_profil:
            self.delete_image(instance.photo_profil.path)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.photo_profil:
            self.delete_image(instance.photo_profil.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete_image(self, image_path):
        if os.path.isfile(image_path):
            os.remove(image_path)
            print(f"Photo supprimée : {image_path}")
        else:
            print(f"Fichier introuvable : {image_path}")
