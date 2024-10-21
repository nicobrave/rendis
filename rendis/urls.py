from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rendiciones.urls')),  # Incluir las URLs de la app rendiciones
]