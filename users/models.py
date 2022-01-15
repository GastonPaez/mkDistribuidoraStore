from django.db import models
from django.contrib.auth.models import AbstractUser

#from django.contrib.auth.models import User

# El modelo convencional genera tgablas en la base de datos y el proxymodel no

#AbstractUser para heredar y modificar atributos por defecto
#Se debe cambiar el User importado en todos los lados que aparece
class User(AbstractUser):

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    def has_shipping_address(self):
        # Si el usuario posee o no una direccion principal
        return self.shipping_address is not None
        




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
