from django.contrib import admin
from .models import Product
# Register your models here.
# Colocar los productos del modelo en el administrador.
class ProductAdmin(admin.ModelAdmin):
    # muestra los campos que se pueden editar
    fields = ('title', 'description', 'image', 'price')
    # muestra los campos que se completan automaticamente en la lista de los productos
    list_display = ('__str__', 'slug', 'created_at')
admin.site.register(Product, ProductAdmin)