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
    weight=models.IntegerField()
    price=models.IntegerField()
    ofr_price=models.IntegerField()
    stock=models.IntegerField()