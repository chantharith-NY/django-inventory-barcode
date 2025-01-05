from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    gender = models.CharField(max_length=1)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    team = models.IntegerField()
    user_profile = models.ImageField(upload_to='profile_images/', default='default.png')
    activation = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='inventory_user_set',  # Add related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='inventory_user_set',  # Add related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self) -> str:
        return f"{self.id} {self.first_name} {self.email} {self.activation}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

class BorrowedItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrowed_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_items')
    quantity = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} borrowed {self.quantity} of {self.item.name}"
    
class ReturnedItem(models.Model):
    id = models.AutoField(primary_key=True)
    borrowed_item = models.ForeignKey(BorrowedItem, on_delete=models.CASCADE, related_name='returned_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='returned_items')
    quantity = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.borrowed_item.user.first_name} returned {self.quantity} of {self.borrowed_item.item.name}"