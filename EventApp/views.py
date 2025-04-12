from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, template_name='EventApp/home.html')

def login(request):
    return render(request, template_name='EventApp/login.html')