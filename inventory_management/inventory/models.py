from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

class Item(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    activation = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            category_code = self.category.name[0].lower()
            last_item = Item.objects.filter(category=self.category).order_by('-id').first()
            if last_item and last_item.id[1:].isdigit():
                last_id = int(last_item.id[1:])
                new_id = f"{category_code}{last_id + 1:03d}"
            else:
                new_id = f"{category_code}001"
            self.id = new_id
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    def is_available(self):
        return not self.borrowed_items.exists()
    

class BorrowedItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrowed_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_items')
    quantity = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    
class ReturnedItem(models.Model):
    id = models.AutoField(primary_key=True)
    borrowed_item = models.ForeignKey(BorrowedItem, on_delete=models.CASCADE, related_name='returned_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='returned_items')
    quantity = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    
class History(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_history')
    returned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='returned_history', null=True, blank=True)
    borrowed_time = models.DateTimeField()
    returned_time = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField()
