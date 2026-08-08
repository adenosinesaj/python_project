from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class C_profile(models.Model):
    ROLE_CHOICES = (
        ('buyer', 'Customer'),
        ('seller', 'Vendor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile/',
        default='profile/user.png',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_role_display()})"


class Product(models.Model):
    STATUS_CHOICES = (
        ('In Stock', 'In Stock'),
        ('Stock Out', 'Stock Out'),
        ('Will be available soon', 'Will be available soon'),
    )

    # Linked seller/vendor to resolve product ownership
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    p_photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='In Stock')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Portfolio(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('canceled', 'Canceled'),
    ]

    # Linked to seller so vendors can showcase their work
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios', null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    event_date = models.DateField()
    location = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='events_images/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='completed')
    team_or_individual = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else f"Portfolio Event #{self.id}"


# ==========================================
# NEW INTERACTIVE EVENT PLANNING MODELS
# ==========================================

class ChecklistTask(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_tasks')
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', 'due_date']

    def __str__(self):
        return f"{self.title} ({'Done' if self.is_completed else 'Pending'})"


class BudgetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_items')
    title = models.CharField(max_length=150)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, blank=True, help_text="Catering, Venue, Decoration")

    def __str__(self):
        return f"{self.title} - Est: {self.estimated_cost} | Act: {self.actual_cost}"


class EventSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    event_name = models.CharField(max_length=150)
    event_date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_name} on {self.event_date.strftime('%Y-%m-%d %H:%M')}"