from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Plato, Resena, Categoria, ItemCarrito, MensajeContacto
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm


# Página principal (index)
def index_view(request):
    destacados = Plato.objects.filter(estado="disponible")[:3]
    return render(request, "menu/index.html", {"destacados": destacados})

# Menú con categorías
def menu_view(request):
    categorias = Categoria.objects.all()
    categoria_nombre = request.GET.get("categoria")

    if categoria_nombre:
        platos = Plato.objects.filter(categoria__nombre__iexact=categoria_nombre, estado="disponible")
    else:
        platos = Plato.objects.filter(estado="disponible")

    return render(
        request, "menu/menu.html", {"categorias": categorias, "platos": platos}
    )


# Listado de clientes
def clientes_view(request):
    clientes = Cliente.objects.all()
    return render(request, "menu/clientes.html", {"clientes": clientes})


# Carrito de compras
def carrito_view(request):
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    
    carrito = request.session['carrito']
    
    # Calcular total
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    
    # AGREGAR AL CARRITO
    if request.method == "POST" and 'plato_id' in request.POST:
        plato_id = request.POST.get("plato_id")
        plato = get_object_or_404(Plato, id=plato_id)
        item_encontrado = None
        for item in carrito:
            if item['plato_id'] == plato.id:
                item_encontrado = item
                break
        
        if item_encontrado:
            item_encontrado['cantidad'] += 1
        else:
            carrito.append({
                'plato_id': plato.id,
                'nombre': plato.nombre,
                'precio': float(plato.precio),
                'cantidad': 1
            })
        
        # GUARDAR EN SESIÓN (IMPORTANTE)
        request.session.modified = True
        messages.success(request, f"¡{plato.nombre} agregado al carrito!")
        return redirect("menu")
    
    # VACIAR CARRITO
    if request.method == "POST" and 'vaciar_carrito' in request.POST:
        request.session['carrito'] = []
        request.session.modified = True
        messages.info(request, "Carrito vaciado")
        return redirect("ver_carrito")
    
    return render(request, "menu/carrito.html", {
        "carrito": carrito,
        "total": total
    })


# Listado y creación de reseñas
def resenas_view(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        comentario = request.POST.get("comentario")
        puntuacion = request.POST.get("puntuacion")
        titulo_plato = request.POST.get("titulo_plato")

        if nombre and email and comentario and puntuacion:
            cliente, _ = Cliente.objects.get_or_create(nombre=nombre, email=email)
            Resena.objects.create(
                cliente=cliente,
                comentario=comentario,
                puntuacion=int(puntuacion),
                titulo_plato=titulo_plato,
            )
            messages.success(request, "¡Reseña agregada correctamente!")
            return redirect("resenas")

    # 🔹 Mostrar reseñas más nuevas primero
    resenas = Resena.objects.select_related("cliente").order_by("-fecha")
    return render(request, "menu/resenas.html", {"resenas": resenas})


# Agregar reseña (página separada)
def agregar_resena_view(request):
    platos = Plato.objects.all()
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        comentario = request.POST.get("comentario")
        puntuacion = request.POST.get("puntuacion")
        plato_id = request.POST.get("plato_id")

        if nombre and email and comentario and puntuacion and plato_id:
            cliente, _ = Cliente.objects.get_or_create(nombre=nombre, email=email)
            plato = get_object_or_404(Plato, id=plato_id)

            Resena.objects.create(
                cliente=cliente,
                titulo_plato=plato.nombre,
                comentario=comentario,
                puntuacion=int(puntuacion),
            )
            messages.success(request, "¡Reseña agregada correctamente!")
            return redirect("resenas")

    return render(request, "menu/agregar_resena.html", {"platos": platos})


# Formulario de contacto
def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            mensaje = form.save()
            
            try:
                send_mail(
                    subject=f"Nuevo mensaje: {mensaje.asunto}",
                    message=f"""
                    Nombre: {mensaje.nombre}
                    Email: {mensaje.email}
                    Teléfono: {mensaje.telefono}
                    
                    Mensaje:
                    {mensaje.mensaje}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["contacto@restauranteoriental.com"],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, '¡Mensaje enviado correctamente!')
            return redirect('contacto')
    else:
        form = ContactoForm()
    
    return render(request, 'menu/contacto.html', {'form': form})