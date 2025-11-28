from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SUV, Deportivo, PickUp, Ford100Anios, SistemaApartado, MetodoPago

# --- Vistas Públicas ---
def inicio(request):
    # Mostramos el último deportivo como "Hero"
    destacado = Deportivo.objects.last()
    return render(request, 'inicio.html', {'destacado': destacado})

def catalogo_suvs(request):
    autos = SUV.objects.all()
    return render(request, 'catalogo.html', {'autos': autos, 'titulo': 'Nuestras SUVs', 'tipo': 'suv'})

def catalogo_deportivos(request):
    autos = Deportivo.objects.all()
    return render(request, 'catalogo.html', {'autos': autos, 'titulo': 'Deportivos de Alto Rendimiento', 'tipo': 'deportivo'})

def catalogo_pickups(request):
    autos = PickUp.objects.all()
    return render(request, 'catalogo.html', {'autos': autos, 'titulo': 'Pick Ups Ford', 'tipo': 'pickup'})

def ford_100_anios(request):
    auto = Ford100Anios.objects.first()
    return render(request, '100_anios.html', {'auto': auto})

# --- Autenticación ---
def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirección inteligente: si es admin va al panel, si no al inicio
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')

def admin_check(request):
    if request.user.is_staff:
        return redirect('/admin/')
    else:
        messages.error(request, "Acceso denegado. Se requieren permisos de administrador.")
        return redirect('login')

# --- Lógica del Carrito ---
@login_required
def agregar_carrito(request, tipo, id_auto):
    carrito = request.session.get('carrito', {})
    
    # Obtener datos del auto según tipo
    auto = None
    if tipo == 'suv': auto = get_object_or_404(SUV, pk=id_auto)
    elif tipo == 'deportivo': auto = get_object_or_404(Deportivo, pk=id_auto)
    elif tipo == 'pickup': auto = get_object_or_404(PickUp, pk=id_auto)
    elif tipo == '100anios': 
        auto = get_object_or_404(Ford100Anios, pk=id_auto)
        # RESTRICCIÓN: Solo 1 por cliente (revisamos historial y carrito)
        ya_comprado = SistemaApartado.objects.filter(id_usuario=request.user, tipo_vehiculo='100anios').exists()
        en_carrito = any(item['tipo'] == '100anios' for item in carrito.values())
        
        if ya_comprado or en_carrito:
            messages.error(request, "Solo se permite una unidad de la Edición 100 Años por cliente.")
            return redirect('100_anios')

    item_id = f"{tipo}_{id_auto}"
    
    if item_id not in carrito:
        carrito[item_id] = {
            'producto_id': id_auto,
            'nombre': auto.nombre,
            'precio': float(auto.precio),
            'cantidad': 1,
            'tipo': tipo,
            'imagen': auto.imagen_url
        }
    else:
        if tipo != '100anios': # No aumentar cantidad si es 100 años (aunque la validación anterior ya lo cubre)
            carrito[item_id]['cantidad'] += 1

    request.session['carrito'] = carrito
    request.session.modified = True
    messages.success(request, f"{auto.nombre} agregado al carrito.")
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

@login_required
def eliminar_carrito(request, item_id):
    carrito = request.session.get('carrito', {})
    if item_id in carrito:
        del carrito[item_id]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('ver_carrito')

@login_required
def checkout(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    if request.method == 'POST':
        metodo = request.POST.get('metodo_pago')
        referencia = request.POST.get('tarjeta', 'Efectivo')
        
        # 1. Guardar Pago
        pago = MetodoPago.objects.create(
            id_usuario=request.user,
            tipo_pago=metodo,
            monto=total,
            referencia=referencia
        )
        
        # 2. Guardar Apartados (Vehículos)
        for key, item in carrito.items():
            SistemaApartado.objects.create(
                nombre_vehiculo=item['nombre'],
                tipo_vehiculo=item['tipo'],
                id_usuario=request.user,
                enganche=item['precio'] * 0.10, # Simulación de enganche
                estado="Apartado"
            )
            
        # 3. Limpiar carrito
        request.session['carrito'] = {}
        request.session.modified = True
        
        return render(request, 'exito.html')

    return render(request, 'checkout.html', {'total': total})