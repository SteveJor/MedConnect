from rest_framework import serializers
from Apps.Prescriptions.models import Ordonnance, Prescription
from Apps.Consultations.models import Consultation

class OrdonnanceSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all())

    class Meta:
        model = Ordonnance
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    ordonnance = serializers.PrimaryKeyRelatedField(queryset=Ordonnance.objects.all())

    class Meta:
        model = Prescription
        fields = '__all__'
