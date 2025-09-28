from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("menu/", views.menu_view, name="menu"),
    path("catalogo/", views.menu_view, name="catalogo"),
    path("contacto/", views.contacto_view, name="contacto"),
    path("clientes/", views.clientes_view, name="clientes"),
    path("carrito/", views.carrito_view, name="ver_carrito"),
    path("clientes/agregar_resena/", views.agregar_resena_view, name="agregar_resena"),
    path("resenas/", views.resenas_view, name="resenas"),
]