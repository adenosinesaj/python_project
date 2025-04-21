from django.shortcuts import render,redirect
from .models import *
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import C_profile
from django.contrib.auth.decorators import login_required
from .form import SignUpForm
from django.contrib import messages



# Create your views here.
def home(request):
    return render(request, template_name='EventApp/home.html')

def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='EventApp/product.html', context = context)

def signup_view(request): 
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # ✅ Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'EventApp/signup.html', {'form': form})

            # ✅ Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'EventApp/signup.html', {'form': form})

            # ✅ Create user and profile
            user = form.save()
            profile_picture = form.cleaned_data.get('profile_picture')
            if not C_profile.objects.filter(user=user).exists():
                C_profile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get('phone', ''),
                    bio=form.cleaned_data.get('bio', ''),
                    profile_picture=profile_picture if profile_picture else 'profile/user.png'
                )
            login(request, user)
            messages.success(request, "Signup successful! Welcome 🎉")
            return redirect('profile')  # Make sure 'profile' is a valid URL name

    else:
        form = SignUpForm()

    return render(request, 'EventApp/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful! Welcome back 😊")

            return redirect('home')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()
    return render(request, 'EventApp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    try:
        profile = C_profile.objects.get(user=request.user)
    except C_profile.DoesNotExist:
        profile = None  # Handle case where profile does not exist

    return render(request, 'EventApp/profile.html', {'profile': profile})


    