from django.contrib import admin
from .models import Categoria, Plato, Cliente, Resena, Contacto, MensajeContacto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "clave")
    search_fields = ("nombre", "clave")


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "categoria", "destacado", "estado")
    list_filter = ("categoria", "estado", "destacado")
    search_fields = ("nombre",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email")
    search_fields = ("nombre", "email")


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "titulo_plato",
        "comentario",
        "puntuacion",
        "fecha",
    )

    list_filter = ("puntuacion",)
    search_fields = ("comentario",)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "mensaje")
    search_fields = ("nombre", "email", "mensaje")


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono", "asunto", "fecha")
    search_fields = ("nombre", "email", "asunto")
    list_filter = ("fecha",)
    ordering = ("-fecha",)
