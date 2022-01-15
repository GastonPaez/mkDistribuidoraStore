from django.db import models
from django.db.models.base import Model
from users.models import User
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed, post_save
import uuid
import decimal
# Create your models here.


class Cart(models.Model):
    # Identificador unico
    cart_id = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    # Relacion con el modelo User
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # comision
    FEE = 0.05

    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        # Se intenta obtener la orden del carrito
        order = self.order_set.first()
        if order:
            # si la orden existe, se actualiza su total
            order.update_total()

    def update_subtotal(self):
        # iterar todos los productos dentro del carrito para obtener su precio
        #self.subtotal = sum([product.price for product in self.products.all()])

        # multiplica el precio del producto por la cantidad
        self.subtotal = sum([
            cp.quantity * cp.product.price for cp in self.products_related()
        ])

        self.save()

    def update_total(self):
        self.total = self.subtotal + \
            (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

        if self.order:
            self.order.update_total()

    def products_related(self):
        # Obtiene los objetos cartproduct y product en la misma consulta
        return self.cartproducts_set.select_related('product')

    @property
    def order(self):
        return self.order_set.first()


class CartProductsManager(models.Manager):
    # Clase para extender los metodos de object

    def create_or_update_quantity(self, cart, product, quantity=1):
        # Si el objeto no existe, se crea.
        # Retorna 2 valores, el objeto y el bolleano True si fue creado.
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:

            # Si el objeto se crea o si se actualiza se va a establecer esta cantidad.
            quantity = object.quantity + quantity

        object.update_quantity(quantity)

        # Retorna el objeto CartProduct
        return object


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()


def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())


def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()


def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()


pre_save.connect(set_cart_id, sender=Cart)
# despues que se haya almacenado
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(update_totals, sender=Cart.products.through)
