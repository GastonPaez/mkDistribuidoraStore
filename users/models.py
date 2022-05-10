from email.policy import default
from operator import truediv
from django.db import models
from django.contrib.auth.models import AbstractUser
from orders.common import OrderStatus

#from django.contrib.auth.models import User

# El modelo convencional genera tgablas en la base de datos y el proxymodel no

#AbstractUser para heredar y modificar atributos por defecto
#Se debe cambiar el User importado en todos los lados que aparece
class User(AbstractUser):
    
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        # Para conocer si posee o no una direccion principal
        return self.shippingaddress_set.filter(default=True).first()
    
    @property
    def billing_profile(self):
        return self.billingprofile_set.filter(default=True).first()

    def has_shipping_address(self):
        # Si el usuario posee o no una direccion principal
        return self.shipping_address is not None
        
    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

    def has_shipping_addresses(self):
        # para concoer si el usuario tiene direcciones
        return self.shippingaddress_set.exists()
    
    
    
    @property
    def addresses(self):
        return self.shippingaddress_set.all()

    @property
    def billing_profiles(self):
        return self.billing_profile_set.all().order_by('-default')







class Customer(User):
    class Meta:
        # Definiendo el proxymode
        proxy = True
    
    def get_product(self):
        # retorna todos los productos adquiridos por el cliente
        return []

class Profile(models.Model):
    # Relacion uno a uno
    # Cuando se elimina un usuario se elimina el profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
