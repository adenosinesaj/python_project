from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
class C_profile(models.Model):
    name= models.CharField(max_length=200)
    age = models.IntegerField(blank=True,null=True)

