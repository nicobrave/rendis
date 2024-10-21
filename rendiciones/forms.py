from django import forms
from .models import Proyecto
from .models import Rendicion

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'jefe_obra', 'google_sheets_url', 'google_sheets_sheet']

class RendicionForm(forms.ModelForm):
    class Meta:
        model = Rendicion
        fields = ['imagen_factura']
        labels = {'imagen_factura': 'Subir imagen de la factura'}