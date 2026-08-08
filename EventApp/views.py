from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Q, F
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Product, Category, C_profile, CartItem, Order, OrderItem, Portfolio,
    ChecklistTask, BudgetItem, EventSchedule
)
from .forms import (
    SignUpForm, UserUpdateForm, ProfileUpdateForm, ProductForm, PortfolioForm,
    ChecklistTaskForm, BudgetItemForm, EventScheduleForm
)


# ==========================================
# PUBLIC & AUTHENTICATION VIEWS
# ==========================================

def home(request):
    return render(request, 'EventApp/home.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome to ManageHoise 🎉")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'EventApp/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect('home')
    
    return render(request, 'EventApp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = C_profile.objects.get_or_create(user=request.user)
    editable = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')
        else:
            messages.error(request, "Please check the form for errors.")
            editable = True
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'EventApp/profile.html', {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'editable': editable
    })


# ==========================================
# PRODUCT & VENDOR MANAGEMENT VIEWS
# ==========================================

def product_list(request):
    products = Product.objects.all()
    user_role = None
    if request.user.is_authenticated:
        try:
            user_role = request.user.profile.role
        except C_profile.DoesNotExist:
            user_role = None

    return render(request, 'EventApp/product.html', {
        'products': products,
        'role': user_role,
    })


def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'EventApp/product_details.html', {'product': product})


@login_required
def add_product(request):
    if hasattr(request.user, 'profile') and request.user.profile.role != 'seller':
        messages.error(request, "Only vendors can add products.")
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'EventApp/add_product.html', {'form': form})


@login_required
def update_product(request, id):
    product = get_object_or_404(Product, pk=id, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'EventApp/add_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('product_list')

    return render(request, 'EventApp/delete_product.html', {'product': product})


def vendor_list(request):
    vendors = C_profile.objects.filter(role='seller')
    return render(request, 'EventApp/vendor_list.html', {'vendors': vendors})


def vendor_profile(request, user_id):
    vendor = get_object_or_404(C_profile, user__id=user_id, role='seller')
    products = Product.objects.filter(seller=vendor.user)
    portfolios = Portfolio.objects.filter(seller=vendor.user)
    return render(request, 'EventApp/vendor_profile.html', {
        'profile': vendor,
        'products': products,
        'portfolios': portfolios
    })


# ==========================================
# CART & CHECKOUT VIEWS
# ==========================================

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.name} to cart.")
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'EventApp/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
@require_POST
def update_cart_quantity(request, item_id):
    """
    AJAX Endpoint to increment/decrement cart quantity dynamically.
    Expects JSON body: {"quantity": integer}
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_qty = int(data.get('quantity', 1))

        if new_qty > 0:
            cart_item.quantity = new_qty
            cart_item.save()
            
            # Compute total price for item if property exists
            item_total = cart_item.total_price if hasattr(cart_item, 'total_price') else (cart_item.product.price * cart_item.quantity)
            
            return JsonResponse({
                'status': 'success',
                'quantity': cart_item.quantity,
                'item_total': float(item_total)
            })
        else:
            cart_item.delete()
            return JsonResponse({'status': 'deleted'})
            
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid payload'}, status=400)


@login_required
def remove_from_cart(request, item_id):
    """
    Handles both AJAX JSON requests and traditional GET/POST HTTP redirects.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    # If the request comes via JavaScript fetch/AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'status': 'deleted'})

    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    order = Order.objects.create(user=request.user, is_paid=True)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    messages.success(request, "Order placed successfully!")
    return redirect('order_history')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'EventApp/order_history.html', {'orders': orders})


# ==========================================
# INTERACTIVE EVENT PLANNING TOOLS
# ==========================================

@login_required
def planner_dashboard(request):
    tasks = ChecklistTask.objects.filter(user=request.user)
    budget_items = BudgetItem.objects.filter(user=request.user)
    schedules = EventSchedule.objects.filter(user=request.user)

    total_est = budget_items.aggregate(Sum('estimated_cost'))['estimated_cost__sum'] or 0
    total_act = budget_items.aggregate(Sum('actual_cost'))['actual_cost__sum'] or 0

    return render(request, 'EventApp/planner_dashboard.html', {
        'tasks': tasks,
        'budget_items': budget_items,
        'schedules': schedules,
        'total_est': total_est,
        'total_act': total_act,
    })


@login_required
def add_checklist_task(request):
    if request.method == 'POST':
        form = ChecklistTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task added!")
    return redirect('planner_dashboard')


@login_required
def toggle_checklist_task(request, pk):
    task = get_object_or_404(ChecklistTask, pk=pk, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('planner_dashboard')


@login_required
def delete_checklist_task(request, pk):
    task = get_object_or_404(ChecklistTask, pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect('planner_dashboard')


@login_required
def add_budget_item(request):
    if request.method == 'POST':
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Budget item added!")
    return redirect('planner_dashboard')


@login_required
def delete_budget_item(request, pk):
    item = get_object_or_404(BudgetItem, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Budget item deleted.")
    return redirect('planner_dashboard')


# ==========================================
# MISCELLANEOUS & STATIC PAGES
# ==========================================

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'EventApp/search_results.html', {'results': results, 'query': query})


def event_list(request):
    events = Portfolio.objects.all()
    return render(request, 'EventApp/event_list.html', {'events': events})


def event_details(request, pk):
    event = get_object_or_404(Portfolio, pk=pk)
    return render(request, 'EventApp/event_details.html', {'event': event})


def policy(request):
    return render(request, 'EventApp/policy.html')


def help_page(request):
    return render(request, 'EventApp/help.html')


def meet_the_team(request):
    return render(request, 'team_profiles/meet_the_team.html')