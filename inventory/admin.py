from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'activation']
    list_filter = ['activation']
    search_fields = ['name']
admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_id', 'quantity', 'activation']
    list_filter = ['category_id', 'activation']
    search_fields = ['name']
admin.site.register(Item, ItemAdmin)

class Borrowed_ItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'user_id', 'quantity', 'date_time', 'activation']
    list_filter = ['item_id', 'user_id', 'date_time', 'activation']
    search_fields = ['item_id', 'user_id']
admin.site.register(Borrowed_Item, Borrowed_ItemAdmin)

class Returned_ItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'user_id', 'quantity', 'date_time', 'activation']
    list_filter = ['item_id', 'user_id', 'date_time', 'activation']
    search_fields = ['item_id', 'user_id']
admin.site.register(Returned_Item, Returned_ItemAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'gender','team', 'activation']
    list_filter = ['activation']
    search_fields = ['name']
admin.site.register(User, UserAdmin)
# Register your models here.  #