from rest_framework import serializers
from Apps.Consultations.models import DemandeConsultation
from Apps.Patients.models import Patient
from Apps.Medical_Personnel.models import MedicalPersonnel
from Apps.Consultations.models import Consultation
from Apps.Medical_Records.models import DossierMedical
class DemandeConsultationSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medical_personnel = serializers.PrimaryKeyRelatedField(queryset=MedicalPersonnel.objects.all(), required=False, allow_null=True)

    class Meta:
        model = DemandeConsultation
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medical_personnel = serializers.PrimaryKeyRelatedField(queryset=MedicalPersonnel.objects.all(), required=False, allow_null=True)
    demande_consultation = serializers.PrimaryKeyRelatedField(queryset=DemandeConsultation.objects.all(), required=False, allow_null=True)
    dossier_medical = serializers.PrimaryKeyRelatedField(queryset=DossierMedical.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Consultation
        fields = '__all__'
