from django.shortcuts import render,redirect
from .models import *
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import C_profile
from .form import ProfilePictureForm
from django.contrib.auth.decorators import login_required
from .form import SignUpForm
from django.contrib import messages






# Create your views here.
def home(request):
    form = AuthenticationForm()
    return render(request, template_name='EventApp/home.html')

def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='EventApp/product.html', context = context)

def cart_view(request):
    # This is a placeholder; replace it with actual logic
    return render(request, 'cart.html')  # Make sure you create cart.html!

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
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Logged in successfully!")
        return redirect('home')
    return render(request, 'EventApp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@login_required
def profile_view(request):
    try:
        profile = C_profile.objects.get(user=request.user)
    except C_profile.DoesNotExist:
        profile = C_profile(user=request.user)
        profile.save()

    editable = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        updated = False

        if request.POST.get('first_name') != profile.user.first_name:
            profile.user.first_name = request.POST.get('first_name')
            updated = True
        if request.POST.get('last_name') != profile.user.last_name:
            profile.user.last_name = request.POST.get('last_name')
            updated = True
        if request.POST.get('phone') != profile.phone:
            profile.phone = request.POST.get('phone')
            updated = True
        if request.POST.get('address') != profile.address:
            profile.address = request.POST.get('address')
            updated = True
        if request.POST.get('bio') != profile.bio:
            profile.bio = request.POST.get('bio')
            updated = True
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            updated = True

        if updated:
            profile.save()
            profile.user.save()
            # Refresh the profile from the DB to ensure updated image URL is used
            profile.refresh_from_db()

    return render(request, 'EventApp/profile.html', {'profile': profile, 'editable': editable})