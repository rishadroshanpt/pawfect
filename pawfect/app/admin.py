from django.contrib import admin
from .models import *
# Register your models here.
admin.register(Pet)
admin.register(Category)
admin.register(Product)
admin.register(Details)
admin.register(Cart)