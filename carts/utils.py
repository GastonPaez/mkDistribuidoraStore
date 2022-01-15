from .models import Cart

def get_or_create_cart(request):
    #request.session['cart_id'] = None
    # Si el Usuario esta autenticado se obtiene el usuario actual
    user = request.user if request.user.is_authenticated else None
    
    cart_id = request.session.get('cart_id') #Retorna None si no existe
    cart = Cart.objects.filter(cart_id=cart_id).first() # Lista de objetos. Si no encuentra retorna None

    # Crea el carrito si no existe
    if cart is None:
        cart = Cart.objects.create(user=user)       

    # Si el usuario existe y el carrito no tiene un usuario
    if user and cart.user is None:
        # Asignar un usuario
        cart.user = user 
        cart.save()
    """
    if cart_id:
        # filtra la busqueda por el pk
        cart = Cart.objects.get(cart_id=cart_id)  
    else:
        cart = Cart.objects.create(user = user)
    """
    # Almacena el id del carrito
    request.session['cart_id'] = cart.cart_id

    return cart 

def destroy_cart(request):
    request.session['cart_id'] = None