from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Crée un routeur par défaut
router = DefaultRouter()

# Enregistre les ViewSets avec le routeur
router.register(r'Utilisateurs', CompteUtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclut les URLs générées par le routeur
    path('login/', LoginView.as_view(), name='login'),
    # ... autres URLs
]