from django.db import models
from django.contrib.auth.models import User

# Clase abstracta para evitar repetir código en vehículos comunes
class VehiculoBase(models.Model):
    nombre = models.CharField(max_length=100)
    anio = models.IntegerField(verbose_name="Año")
    color = models.CharField(max_length=50)
    motor = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField(max_length=500, verbose_name="URL de Imagen")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombre} - {self.anio}"

class SUV(VehiculoBase):
    id_suv = models.AutoField(primary_key=True)
    class Meta: verbose_name = "SUV"

class Deportivo(VehiculoBase):
    id_deportivo = models.AutoField(primary_key=True)
    class Meta: verbose_name = "Deportivo"

class PickUp(VehiculoBase):
    id_pickup = models.AutoField(primary_key=True)
    class Meta: verbose_name = "Pick Up"

class Ford100Anios(models.Model):
    id_aniversario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, default="Mustang Edición Centenario")
    motor = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    rines = models.CharField(max_length=100)
    emblemas = models.CharField(max_length=200)
    interior = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    disponible = models.BooleanField(default=True)
    imagen_url = models.URLField(max_length=500)

    class Meta:
        verbose_name = "Ford 100 Años"
        verbose_name_plural = "Ford 100 Años"

    def __str__(self):
        return "Edición Centenario"

class SistemaApartado(models.Model):
    id_apartado = models.AutoField(primary_key=True)
    # Guardamos referencia del vehículo como texto para simplificar la mezcla de tablas
    nombre_vehiculo = models.CharField(max_length=150) 
    tipo_vehiculo = models.CharField(max_length=50) # SUV, Deportivo, etc.
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_apartado = models.DateTimeField(auto_now_add=True)
    enganche = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=50, default="Pendiente")

    def __str__(self):
        return f"Apartado {self.id_apartado} - {self.id_usuario.username}"

class MetodoPago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=50) # Efectivo, Tarjeta
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    estado_pago = models.CharField(max_length=50, default="Exitoso")

    def __str__(self):
        return f"Pago {self.id_pago} - {self.monto}"