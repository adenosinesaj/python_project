from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, template_name='EventApp/home.html')

def login(request):
    return render(request, template_name='EventApp/login.html')

def C_profile(request):
    return render(request, template_name='EventApp/C_profile.html')
def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='EventApp/product.html', context = context)

