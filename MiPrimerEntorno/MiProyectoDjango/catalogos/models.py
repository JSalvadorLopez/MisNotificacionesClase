from django.db import models

# Create your models here.
class Categoria(models.Model):
	categoria = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255)

	def __str__(self):
		return self.categoria

class Producto(models.Model):
	categoria = models.ForeignKey(Categoria)
	producto = 	models.CharField("Nombre del producto",max_length=60)
	existencia = models.IntegerField("Existencia en almacen")
	defectos = 	models.IntegerField("Productos defectuosos")
	pMayoreo = 	models.DecimalField("Precio Mayoreo", max_digits=6, decimal_places=2)
	pMedMay = 	models.DecimalField("Precio Medio Mayoreo", max_digits=6, decimal_places=2)
	pMenudeo = 	models.DecimalField("Precio Menudeo", max_digits=6, decimal_places=2)
	imagen = models.ImageField(blank=True)

	def __str__(self):
		return self.producto