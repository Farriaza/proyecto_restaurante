from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    NOMBRES = [
        ("colaciones", "Colaciones"),
        ("platos", "Platos (2-10 personas)"),
        ("bebestibles", "Bebestibles"),
        ("acompanamientos", "Acompañamientos"),
    ]
    clave = models.CharField(max_length=50, choices=NOMBRES, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    ESTADO_CHOICES = (
        ("disponible", "Disponible"),
        ("agotado", "Agotado"),
    )

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # texto libre
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        "Categoria", on_delete=models.SET_NULL, null=True, blank=True
    )
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField(
        upload_to="platos/", blank=True, null=True
    )  # 🔹 nuevo campo
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="disponible"
    )

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Resena(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comentario = models.TextField(default="Sin comentario")  # 🔹 evita null
    puntuacion = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)  # 🔹 ordenaremos con este
    titulo_plato = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.puntuacion}⭐"


class Contacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.email}"


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"


#Agregado sistema de carrito
class ItemCarrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"

    class Meta:
        unique_together = ['cliente', 'plato']