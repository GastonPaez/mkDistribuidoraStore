from .models import Order
from django.urls import reverse


def get_or_create_order(cart, request):
    # La orden hereda del carrito de compras

    # Se centraliza la orden con respecto al carrito
    order = cart.order

    # Si la orden no existe y el usuario esta autenticado
    if order is None and request.user.is_authenticated:
        # Se crea una orden asignando el carrito y el usuario authenticado
        order = Order.objects.create(cart=cart, user=request.user)

    # Si la orden existe se actualiza la sesion
    if order:
        request.session['order_id'] = order.order_id

    return order


def breadcrumb(products=True, address=False, payment=False, confirmation=False):
    return [
        {
            'title': 'Productos',
            'active': products,
            'url': reverse('orders:order')
        },
        {
            'title': 'Direccion',
            'active': address,
            'url': reverse('orders:address')
        },
        {
            'title': 'Pago',
            'active': payment,
            'url': reverse('orders:payment')
        },
        {
            'title': 'Confirmacion',
            'active': confirmation,
            'url': reverse('orders:confirm')
        }
    ]

def destroy_order(request):
    request.session['order_id'] = None
    
