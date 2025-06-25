from rest_framework import serializers
from .models import Patient  # Ou selon ton chemin exact
from Apps.Users.models import CompteUtilisateur  # Modèle utilisateur

class PatientSerializer(serializers.ModelSerializer):
    compteUtilisateur = serializers.PrimaryKeyRelatedField(queryset=CompteUtilisateur.objects.all(), required=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def validate_poids(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Le poids doit être un nombre positif.")
        return value

    def validate_taille(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("La taille doit être un nombre positif.")
        return value
