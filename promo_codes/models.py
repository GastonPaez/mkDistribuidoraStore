from time import timezone
from django.db import models
from django.db.models.signals import pre_save
import string
import random
from django.utils import timezone
# Create your models here.

class PromoCodeManager(models.Manager):

    def get_valid(self, code):
        now = timezone.now()
        # Filtra el codigo promocional si es valido filtrando si fue usado o si esta expirado
        return self.filter(code=code).filter(used=False).filter(valid_from__lte=now).filter(valid_to__gte=now).first()

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(default=0.0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    objects = PromoCodeManager()

    def __str__(self):
        return self.code
    
    def use(self):
        # para saber si el codigo promocional fue utilizado o no
        self.used = True
        self.save()

def set_code(sender, instance, *args, **kwargs):
    if instance.code:
        return 
    # Genera el codigo promocional de forma aleatoria
    chars = string.ascii_uppercase + string.digits
    instance.code = ''.join(random.choice(chars) for _ in range(10))
        
         

# antes de que un objeto PromoCode ejecute el save, se ejecute el callback set_code
pre_save.connect(set_code, sender=PromoCode)
        