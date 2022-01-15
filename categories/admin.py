from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'description')    
    list_display = ('__str__', 'description')

admin.site.register(Category, CategoryAdmin)