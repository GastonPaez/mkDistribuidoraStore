from enum import Enum, Flag
from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields import CharField
from users.models import User
from carts.models import Cart

from django.db.models.signals import pre_save
import uuid
from shipping_addresses.models import ShippingAddress
from .common import OrderStatus, choices
# Create your models here.

class Order(models.Model):
    order_id = CharField(max_length=100, null=False, blank=False, unique=True)
    # Relacion con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relacion uno a muchos con el carrito
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    status = CharField(max_length=50, choices=choices,
                       default=OrderStatus.CREATED)  # Enum
    shipping_total = models.DecimalField(
        default=5, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def get_or_set_shipping_address(self):
        # Si la orden posee una direccion de envio la va a retornar, sino 
        if self.shipping_address:
            return self.shipping_address

        # Obtiene la direccion principal del usuario
        shipping_address = self.user.shipping_address
        if shipping_address:
            self.update_shipping_address(shipping_address)
        return shipping_address

    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_total(self):
        return self.cart.total + self.shipping_total


# Establece un valor para el identificador unico, a traves de un callback y un signal pre_save
def set_order_id(sender, instance, *args, **kwargs):
    # Si la orden no posee el order_id
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, sender=Order)
# Antes de que un objeto order se almacene, se ejecuta el callback
pre_save.connect(set_total, sender=Order)
