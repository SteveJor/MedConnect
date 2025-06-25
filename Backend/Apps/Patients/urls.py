from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, RegisterPatientView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')

urlpatterns = router.urls +  [
    path("register_patient/", RegisterPatientView.as_view(), name="register_patient"),
]

