"""
Configuration des URLs du projet Backend.

La liste `urlpatterns` sert à router les requêtes HTTP vers les vues appropriées.

Chaque `path()` associe une URL de base à une application Django spécifique via la fonction `include()`,
ou à une vue directement (comme l'admin Django).

Les applications sont exposées sous le préfixe 'api/' pour toutes les API REST.

La gestion des fichiers médias en développement est assurée par la fonction `static()`.

Pour plus d'infos :
https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Apps.Consultations.urls')),
    path('api/', include('Apps.Medical_Personnel.urls')),
    path('api/', include('Apps.Medical_Records.urls')),
    path('api/', include('Apps.Patients.urls')),
    path('api/', include('Apps.Prescriptions.urls')),
    path('api/', include('Apps.Users.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)