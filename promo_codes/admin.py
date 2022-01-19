from django.contrib import admin
from .models import PromoCode
# Register your models here.

class PromoCodeAdmin(admin.ModelAdmin):
    # Se quita la posibilidad de editar o crear un promo_code
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)