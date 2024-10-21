from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('jefe_obra', 'Jefe de Obra'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    jefe_obra = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'jefe_obra'})
    google_sheets_url = models.URLField()
    google_sheets_sheet = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Rendicion(models.Model):
    jefe_obra = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen_factura = models.ImageField(upload_to='rendiciones/')  # Guardar en la carpeta 'rendiciones'
    fecha_subida = models.DateTimeField(auto_now_add=True)
    google_sheets_url = models.URLField()  # URL a la hoja de cálculo
    google_sheets_sheet = models.CharField(max_length=100)  # Nombre de la hoja de cálculo

    def __str__(self):
        return f"Rendición de {self.jefe_obra.username} - {self.fecha_subida}"
