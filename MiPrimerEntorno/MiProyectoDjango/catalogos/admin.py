from django.contrib import admin
from .models import Categoria, Producto

# Register your models here.
admin.site.register(Categoria)

@admin.register(Producto)
class AdminProducto(admin.ModelAdmin):
	list_display = ("producto","categoria","existencia", "pMenudeo",)
	list_filter = ("categoria",)