from django.db import models
from django.shortcuts import redirect, render
from .models import Cart
from .utils import get_or_create_cart
from products.models import Product
from django.shortcuts import get_object_or_404
from .models import CartProducts
# Create your views here.


def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        'cart': cart

    })


def add(request):
    # se obtiene el carrito de compras
    cart = get_or_create_cart(request)
    # Busca la pk en el html con la etiqueta que tenga value product_id
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    # Toma del formalario quantity la cantidad de productos y por default es 1
    quantity = int(request.POST.get('quantity', 1))

    """
    # Agrega el objeto como si se tratara de una lista
    cart.products.add(product, through_defaults={
        'quantity':quantity
    }
    )
    """
    #
    cart_product = CartProducts.objects.create_or_update_quantity(
        cart=cart, product=product, quantity=quantity)

    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'cart_product': cart_product,
        'product': product
    })


def remove(request):
    # se obtiene el carrito de compras
    cart = get_or_create_cart(request)

    # se ubica el producto que se quiere eliminar
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    # Quita el producto del carrito de compras
    cart.products.remove(product)

    return redirect('carts:cart')
