from django.db import models
from django.db.models.base import Model
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    slug = models.SlugField(null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='products/' , null=False, blank= False)
    created_at = models.TimeField(auto_now_add=True)

    """
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)
    """
    def __str__(self):
        return self.title        

def set_slug(sender, instance, *args, **kwargs): # Debe recibir 5 elementos
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        
        # si existe algun producto con ese slug, genera uno nuevo
        while Product.objects.filter(slug=slug).exists():
            # pone caracteres aleatorios con la libreria uuid
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8]  )
            )
        # La instancia es nuestro producto almacenado
        instance.slug = slug

# Antes que un objeto product se almacene, ejecuta el callback set_slug
pre_save.connect(set_slug, sender=Product)
    

