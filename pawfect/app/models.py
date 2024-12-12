from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    # pro_id=models.TextField()
    pet=models.TextField()
    category=models.TextField()
    name=models.TextField()
    price=models.IntegerField()
    ofr_price=models.IntegerField()
    img=models.FileField()
    dis=models.TextField()