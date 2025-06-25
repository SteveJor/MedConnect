from rest_framework.routers import DefaultRouter
from Apps.Consultations.views import DemandeConsultationViewSet, ConsultationViewSet

router = DefaultRouter()
router.register(r'demandes-consultation', DemandeConsultationViewSet, basename='demandeconsultation')
router.register(r'consultations', ConsultationViewSet, basename='consultation')

urlpatterns = router.urls
