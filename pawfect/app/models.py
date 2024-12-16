from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category=models.TextField()
    def __str__(self):
        return self.category

class Pet(models.Model):
    pet=models.TextField()
    def __str__(self):
        return self.pet

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE)
    name=models.TextField()
    img=models.FileField()
    dis=models.TextField()

class Details(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    weight=models.IntegerField()
    price=models.IntegerField()
    ofr_price=models.IntegerField()
    stock=models.IntegerField()