from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register([Category, Product,C_profile, Portfolio, CartItem, Order, OrderItem])
