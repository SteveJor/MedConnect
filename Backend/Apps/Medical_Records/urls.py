from rest_framework.routers import DefaultRouter
from Apps.Medical_Records.views import DossierMedicalViewSet

router = DefaultRouter()
router.register(r'dossiers-medicaux', DossierMedicalViewSet, basename='dossiermedical')

urlpatterns = router.urls
