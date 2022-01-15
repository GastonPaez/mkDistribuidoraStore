from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import reverse
from django.views.generic import ListView
from .forms import ShippingAddressForm
from shipping_addresses.models import ShippingAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order


class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def query_set(self):
        # Obtiene todas las direcciones del usuario autenticado
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')


class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    # Utiliza los objetos del modelo ShippingAddress
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'
    success_message = 'Direccion Actualizada exitosamente'

    # Retorna a una url luego de que la modificacion haya sido exitosa
    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario que realizo la peticion no le corresponde la direccion dirreciona al carrito.
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        # Si el objeto (shipping_address) posee ordenes.
        if self.get_object().has_orders():
            return redirect('shipping_addresses:shipping_addresses')

        
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        
        # Si no posee una direccion principal, se establece como verdadera
        shipping_address.default = not request.user.has_shipping_address()
        # Si existen direcciones de este usuario default es falso.
        #shipping_address.default = not ShippingAddress.objects.filter(
        #    user=request.user).exists()

        # Almacena la direccion
        shipping_address.save()

        # Si la peticion posee el parametro next
        if request.GET.get('next'):
            # Si el usuario se encuentra en la orden de compra
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)
                # se establece la direccion recien creada a la orden                
                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion creada exitosamente')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })

def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    # Si la direccion la creo el usuario, puede editarla
    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    
    # si el usuario posee una direccion por default
    if request.user.has_shipping_address():
        # retorna la direccion principal del usuario y la convierte en falsa.
        request.user.shipping_address.update_default()
    # Selecciona la direccion como principal
    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')