from rest_framework.routers import DefaultRouter
from Apps.Prescriptions.views import OrdonnanceViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'ordonnances', OrdonnanceViewSet, basename='ordonnance')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = router.urls
