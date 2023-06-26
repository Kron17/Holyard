from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#ES DONDE SE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length = 50)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField()
    imagen = models.ImageField(null=True, blank=True)
    vigente = models.BooleanField()
    usuarios = models.ManyToManyField(User, through='ItemsCarrito')

    def __str__(self):
        return self.nombre

class ItemsCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_agregada = models.IntegerField(default=0)

    class Meta:
        db_table = "db_items_carrito"


class HistorialCompra(models.Model):
    codigo_compra = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo_compra:
            last_purchase = HistorialCompra.objects.order_by('-id').first()
            if last_purchase:
                last_code = int(last_purchase.codigo_compra.lstrip('#'))
                new_code = last_code + 1
            else:
                new_code = 100
            self.codigo_compra = f"#{new_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo_compra
    
class Suscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField(null=True)
    estado = models.BooleanField(default=False)