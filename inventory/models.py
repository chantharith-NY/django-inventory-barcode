from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    activation = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_items')
    quantity = models.IntegerField()
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.name) + ' ' + str(self.category_id) + ' ' + str(self.quantity) + ' ' + str(self.activation)
    
class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    gender = models.CharField(max_length=1)
    email = models.EmailField()
    birth_date = models.DateField()
    team = models.IntegerField()
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.name) + ' ' + str(self.email) + ' ' + str(self.activation)
class Borrowed_Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_items')
    user_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='user_items')
    quantity = models.IntegerField()
    date_time = models.DateTimeField()
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.item_id) + ' ' +str(self.user_id)+ ' ' + str(self.quantity) + ' ' + ' '+ str(self.date_time)+ str(self.activation)
    
class Returned_Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_id')
    user_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='user_id')
    quantity = models.IntegerField()
    date_time = models.DateTimeField()
    activation = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.item_id) + ' ' +str(self.user_id)+ ' ' + str(self.quantity) + ' ' + ' '+ str(self.date_time)+ str(self.activation)