from django.db import models
from django.contrib.auth.models import User

# Category model to categorize products
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
# # Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    status_choice = (
        ('In Stock', 'In Stock'),
        ('Stock Out', 'Stock Out'),
        ('Will be available soon', 'Will be available soon'),
    )
    status = models.CharField(max_length=100, choices=status_choice, default='In Stock')

    def __str__(self):
        return self.name    
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



# C_profile model to store user profile information
class C_profile(models.Model):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile/',
        default='profile/user.png',  # Set default image path
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)  # Add address field

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
# Event model to store event information
class  Portfolio (models.Model):
    image = models.ImageField(upload_to='events_images/', null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    event_date = models.DateField()
    location = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('canceled', 'Canceled'),
    ], default='completed')
    team_or_individual = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Event"



   