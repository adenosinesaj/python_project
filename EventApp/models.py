from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

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
