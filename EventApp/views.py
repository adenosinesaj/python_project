from django.shortcuts import render,redirect
from .models import *
from django.utils.timezone import now
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import C_profile
from .form import *
from django.contrib.auth.decorators import login_required
from .form import SignUpForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404





def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product') 
    context = {'form': form}    
    return render(request, 'EventApp/add_product.html', context=context) 

def update_product(request, id):
    product = Product.objects.get(pk = id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product')
    conext = {'form': form}
    return render(request, template_name= 'EventApp/add_product.html', context=conext)

def delete_product(request, id):
    product = Product.objects.get(pk = id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product')
    context = {'product': product}
    return render(request, template_name='EventApp/delete_product.html', context=context)



# Create your views here.
def home(request):
    form = AuthenticationForm()
    return render(request, template_name='EventApp/home.html')

def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='EventApp/product.html', context = context)

def policy(request):
    return render(request , 'EventApp/policy.html')

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results})
def cart(request):
    # This is a placeholder; replace it with actual logic
    return render(request, 'EventApp/cart.html')  # Make sure you create cart.html!
def product_details(request, id):
    product = Product.objects.get(pk = id)
    context = {'product': product}
    return render(request,template_name = 'EventApp/product_details.html', context = context)

def meet_the_team(request):
    return render(request, template_name='team_profiles/meet_the_teem.html')

def profile_sajid(request):
    return render(request, template_name='team_profiles/profile_sajid.html')

def profile_toma(request):
    return render(request, template_name='team_profiles/profile_toma.html')


def event_list(request):
    events = Portfolio.objects.all()
    return render(request, 'EventApp/event_list.html', {'events': events})

def event_details(request, pk):
    event = get_object_or_404(Portfolio, pk=pk)
    return render(request, 'EventApp/event_details.html', {'event': event})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'EventApp/signup.html', {'form': form})

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'EventApp/signup.html', {'form': form})

            # Create user manually instead of form.save()
            user = User(
                username=username,
                email=email,
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Get the role and other fields
            role = request.POST.get('role')
            phone = form.cleaned_data.get('phone')
            profile_picture = form.cleaned_data.get('profile_picture') or 'profile/user.png'
            bio = form.cleaned_data.get('bio')

            # Save profile
            C_profile.objects.create(
                user=user,
                phone=phone,
                profile_picture=profile_picture,
                bio=bio,
                role=role
            )

            login(request, user)
            messages.success(request, "Signup successful! Welcome 🎉")
            return redirect('home')

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
            messages.success(request, "Profile updated successfully!")

    return render(request, 'EventApp/profile.html', {'profile': profile, 'editable': editable})