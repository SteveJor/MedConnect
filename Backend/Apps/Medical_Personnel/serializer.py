from rest_framework import serializers
from .models import MedicalPersonnel
from Apps.Patients.models import Patient

class MedicalPersonnelSerializer(serializers.ModelSerializer):
    comptePatientLie = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = MedicalPersonnel
        fields = '__all__'

    def validate_annee_exercice(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value is not None and (value < 1900 or value > current_year):
            raise serializers.ValidationError("L'année d'exercice est invalide.")
        return value

    def validate_photo_profil(self, value):
        if value and not value.content_type.startswith('image/'):
            raise serializers.ValidationError("Le fichier téléchargé doit être une image.")
        return value
