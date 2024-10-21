from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import ProyectoForm
from .models import Rendicion, Proyecto 
from .forms import RendicionForm
from .google_vision import process_receipt 
from .google_sheets import save_to_google_sheets 


# Vista para la página de inicio
def index(request):
    return redirect('login')


# Función para verificar si un usuario es admin
def admin_required(user):
    return user.is_authenticated and user.role == 'admin'


# Función para verificar si un usuario es jefe de obra
def jefe_required(user):
    return user.is_authenticated and user.role == 'jefe_obra'


# Dashboard para el administrador
@user_passes_test(admin_required)
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


# Dashboard para el jefe de obra
@user_passes_test(jefe_required)
@login_required
def jefe_dashboard(request):
    return render(request, 'jefe_dashboard.html')


# Redirige al usuario según su rol después de iniciar sesión
@login_required
def redirect_user(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'jefe_obra':
        return redirect('jefe_dashboard')
    else:
        return redirect('login')


# Vista para que el administrador cree proyectos
@user_passes_test(admin_required)
@login_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')  # Redirigir a la lista de proyectos
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})


# Vista para listar los proyectos
@user_passes_test(admin_required)
@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'lista_proyectos.html', {'proyectos': proyectos})

@user_passes_test(jefe_required)
@login_required
def subir_rendicion(request):
    proyecto = get_object_or_404(Proyecto, jefe_obra=request.user)
    if request.method == 'POST':
        form = RendicionForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data['imagen_factura']
            # Procesar la imagen con Google Vision
            datos_factura = process_receipt(imagen)
            # Guardar la rendición en la base de datos
            rendicion = form.save(commit=False)
            rendicion.jefe_obra = request.user
            rendicion.google_sheets_url = proyecto.google_sheets_url
            rendicion.google_sheets_sheet = proyecto.google_sheets_sheet
            rendicion.save()

            # Guardar los datos en Google Sheets
            save_to_google_sheets(
                uid=request.user.id,
                email=request.user.email,
                project_id=proyecto.id,
                provider_name=datos_factura['provider_name'],
                document_type="Factura",
                detail=datos_factura['detail'],
                document_number=datos_factura['document_number'],
                document_date=datos_factura['document_date'],
                total_amount=datos_factura['total_amount'],
                google_sheet_url=proyecto.google_sheets_url,
                sheet_name=proyecto.google_sheets_sheet,
                item_number=rendicion.id  # Usamos el ID de la rendición como número secuencial
            )
            return redirect('lista_rendiciones')
    else:
        form = RendicionForm()

    rendiciones = Rendicion.objects.filter(jefe_obra=request.user).order_by('-fecha_subida')
    return render(request, 'subir_rendicion.html', {'form': form, 'rendiciones': rendiciones})

# Eliminar una rendición
@user_passes_test(jefe_required)
@login_required
def eliminar_rendicion(request, rendicion_id):
    rendicion = get_object_or_404(Rendicion, id=rendicion_id, jefe_obra=request.user)
    if request.method == 'POST':
        rendicion.delete()
        return redirect('lista_rendiciones')
    return render(request, 'confirmar_eliminar.html', {'rendicion': rendicion})