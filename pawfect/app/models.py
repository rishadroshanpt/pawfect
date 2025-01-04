from django.db import models
from django.contrib.auth.models import User

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
