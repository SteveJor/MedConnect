from rest_framework import serializers
from Apps.Medical_Records.models import DossierMedical
from Apps.Patients.models import Patient

class DossierMedicalSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = DossierMedical
        fields = '__all__'

    def validate(self, data):
        # S'assurer qu’un patient n’a pas déjà un dossier
        if self.instance is None:
            patient = data.get('patient')
            if DossierMedical.objects.filter(patient=patient).exists():
                raise serializers.ValidationError("Ce patient possède déjà un dossier médical.")
        return data
