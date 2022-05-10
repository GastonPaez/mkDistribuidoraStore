from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product
from django.views.generic.detail import DetailView
from django.db.models import Q #Ejecuta consulta aplicando diferentes filtros
# Create your views here.
class ProductListView(ListView):
    # Al importar de listview hay que definir 2 atributos
    template_name = 'index.html'
    # La consulta para obtener el listado de objetos
    queryset = Product.objects.all().order_by('-id')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['product_list']
        return context

class ListProduct(ListView):
    template_name = 'webproducts.html'
    # La consulta para obtener el listado de objetos
    queryset = Product.objects.all().order_by('-id')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['product_list']
        return context


class ProductDetailView(DetailView):
    # Obtiene un objeto y un registro mediante un identificador por default
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print(context)
        return context


class ProductSearchListView(ListView):
    template_name= 'products/search.html'
    
    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        # Realiza la consulta conteniendo alguna letra que se coloca en el buscador a partir de lo que nos envia el formulario en self.query
        return Product.objects.filter(filters)

    def query(self):        
        return self.request.GET.get('q')
        # Muestra el resultado en el template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()

        return context
        