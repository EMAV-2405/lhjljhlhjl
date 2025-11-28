from django.contrib import admin
from .models import SUV, Deportivo, PickUp, Ford100Anios, SistemaApartado, MetodoPago

# Personalización del Header
admin.site.site_header = "Administración Ford México"
admin.site.site_title = "Panel Ford"
admin.site.index_title = "Gestión de Vehículos y Ventas"

@admin.register(SUV)
class SUVAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio', 'precio', 'color')

@admin.register(Deportivo)
class DeportivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio', 'precio', 'color')

@admin.register(PickUp)
class PickUpAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'anio', 'precio', 'color')

@admin.register(Ford100Anios)
class Ford100AniosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'disponible', 'precio')

@admin.register(SistemaApartado)
class SistemaApartadoAdmin(admin.ModelAdmin):
    list_display = ('id_apartado', 'nombre_vehiculo', 'id_usuario', 'fecha_apartado')
    list_filter = ('fecha_apartado',)

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'id_usuario', 'monto', 'tipo_pago', 'fecha_pago')