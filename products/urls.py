from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
     #pk es primary key la llave primaria
    path('search', views.ProductSearchListView.as_view(), name='search' ),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product' ),
    
]