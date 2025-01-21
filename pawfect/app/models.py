from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

# Create your models here.


class Pet(models.Model):
    pet=models.TextField()
    img=models.FileField()

class Category(models.Model):
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE)

    category=models.TextField()
    img=models.FileField()

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name=models.TextField()
    img=models.FileField()
    dis=models.TextField()

class Details(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    dis=models.TextField()
    price=models.IntegerField()
    ofr_per=models.FloatField()
    ofr_price=models.FloatField()
    stock=models.IntegerField()

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro=models.ForeignKey(Details,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.FloatField()

class Fav(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro=models.ForeignKey(Product,on_delete=models.CASCADE)

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField()
    phn=models.IntegerField()
    house=models.TextField()
    street=models.TextField()
    pin=models.IntegerField()
    state=models.TextField()
    
class Bookings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pro=models.ForeignKey(Details,on_delete=models.CASCADE)
    qty=models.TextField()
    price=models.FloatField()
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(_("Payment Status"), default=PaymentStatus.PENDING,max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    signature_id = models.CharField(_('Signature ID'),max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"