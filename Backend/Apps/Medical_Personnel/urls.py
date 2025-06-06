from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Crée un routeur par défaut
router = DefaultRouter()

# Enregistre les ViewSets avec le routeur
# router.register(r'Utilisateurs', )

urlpatterns = [
    # ... autres URLs
]