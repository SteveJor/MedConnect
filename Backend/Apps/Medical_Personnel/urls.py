from rest_framework.routers import DefaultRouter
from .views import MedicalPersonnelViewSet

router = DefaultRouter()
router.register(r'medical-personnels', MedicalPersonnelViewSet, basename='medicalpersonnel')

urlpatterns = router.urls
