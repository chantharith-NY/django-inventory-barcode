from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import JsonResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.utils.functional import SimpleLazyObject
import json
from django.utils import timezone
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
# from .models import UserProfile

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventory/dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "inventory/login.html")

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add(request):
    if request.method == "POST":
        if 'category_name' in request.POST:
            category_name = request.POST.get('category_name')
            description = request.POST.get('description')
            if Category.objects.filter(name=category_name).exists():
                messages.error(request, "Category already exists!")
            else:
                category = Category.objects.create(name=category_name, description=description)
                category.save()
                messages.success(request, "Category added successfully!")
        elif 'name' in request.POST:
            item_name = request.POST.get('name')
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)
            item=Item.objects.create(name=item_name, category=category)
            item.save()
            messages.success(request, "Item added successfully!")
        return redirect('inventory:add')
    categories = Category.objects.all()
    return render(request, 'inventory/add.html', {'categories': categories})

@login_required
def display(request):
    if request.method == "POST" and 'update_item' in request.POST:
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        item.name = request.POST.get('name')
        item.category_id = request.POST.get('category')
        item.save()
        messages.success(request, "Item updated successfully!")
        return redirect('inventory:display')
    
    items = Item.objects.all()
    categories = Category.objects.all()
    return render(request, 'inventory/display.html', {'items': items, 'categories': categories})

@login_required
@user_passes_test(is_superuser)
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully!")
    return redirect('inventory:display')

@login_required
def dashboard(request):
    user = request.user
    borrowed_item_ids = BorrowedItem.objects.values_list('item_id', flat=True)
    available_items = Item.objects.exclude(id__in=borrowed_item_ids)
    borrowed_items = BorrowedItem.objects.all()
    return render(request, 'inventory/dashboard.html', {
        'available_items': available_items,
        'borrowed_items': borrowed_items,
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL,
    })

@login_required
@user_passes_test(is_superuser)
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = '12345'
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        
        if is_superuser:
            prefix = 'admin.'
            user_count = User.objects.filter(is_superuser=True).count() + 1
            username = f"{prefix}{last_name}"
        elif is_staff:
            prefix = ''
            user_count = User.objects.filter(is_staff=True, is_superuser=False).count() + 1
            username = f"{prefix}{last_name}{user_count:03d}"
        
        else:
            prefix = 'admin.'
            user_count = User.objects.filter(is_superuser=True).count() + 1
            username = f"{prefix}{last_name}"
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        messages.success(request, "User added successfully!")
        return redirect('inventory:add_user')
    return render(request, 'inventory/add_user.html')

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and password == confirm_password:
            user.set_password(password)
            update_session_auth_hash(request, user)
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('inventory:profile')
    return render(request, 'inventory/profile.html', {'user': user})

@login_required
@user_passes_test(is_superuser)
def display_user(request):
    if request.method == "POST" and 'edit_user' in request.POST:
        user_id = request.POST.get('id')
        user = get_object_or_404(User, id=user_id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        last_name = user.last_name.lower()
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and password == confirm_password:
            user.set_password(password)
            update_session_auth_hash(request, user)
        
        if user.is_superuser:
            prefix = 'admin.'
            user_count = User.objects.filter(is_superuser=True).count() + 1
            user.username = f"{prefix}{last_name}"
            user.set_password(password)
            update_session_auth_hash(request, user)
            user.save()
        
        if user.is_staff:
            prefix = ''
            user_count = User.objects.filter(is_staff=True, is_superuser=False).count() + 1
            user.username = f"{prefix}{last_name}"
            user.set_password(password)
            update_session_auth_hash(request, user)
            user.save()
            
        if user.is_superuser and user.is_staff:
            prefix = 'admin.'
            user_count = User.objects.filter(is_superuser=True).count() + 1
            user.username = f"{prefix}{last_name}"
            user.set_password(password)
            update_session_auth_hash(request, user)
            user.save()
        messages.success(request, "User updated successfully!")
        return redirect('inventory:display_users')
    users = User.objects.all()
    return render(request, 'inventory/display_users.html', {'users': users})

@login_required
@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('inventory:display_users')

@login_required
@user_passes_test(is_superuser)
def edit_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        # Only update the username if it's not the current user
        password_form = AdminPasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Password updated successfully!')
        
        user.save()
        
        # Update the session auth hash to prevent logout
        if request.user.id == user.id:
            update_session_auth_hash(request, user)
        return JsonResponse({'message': 'User updated successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def barcode_scan(request):
    item = None
    error_message = None
    if request.method == "POST":
        barcode_data = request.POST.get('barcode')
        
        # Fetch item information based on barcode data
        try:
            item = Item.objects.get(id=barcode_data)
        except Item.DoesNotExist:
            error_message = 'Item not found'
    return render(request, 'inventory/barcode_scan.html', {'item': item, 'error_message': error_message})

@csrf_exempt
def borrow_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if not item.is_available():
        messages.error(request, 'Item is already borrowed.')
        return redirect('inventory:barcode_scan')
    user = request.user
    print(f"Borrowing item: {item.id} by user: {user.id}")  # Debugging statement
    BorrowedItem.objects.create(item=item, user=user, quantity=1)
    History.objects.create(item=item, borrowed_by=user, borrowed_time=timezone.now(), quantity=1)
    messages.success(request, 'Item borrowed successfully!')
    return redirect('inventory:barcode_scan')

@login_required
@csrf_exempt
def return_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user = request.user
    borrowed_item = BorrowedItem.objects.filter(item=item).first()
    if borrowed_item:
        print(f"Returning item: {item.id} by user: {user.id}")  # Debugging statement
        ReturnedItem.objects.create(borrowed_item=borrowed_item, user=user, quantity=borrowed_item.quantity)
        history_record = History.objects.filter(item=item, returned_time__isnull=True).first()
        if history_record:
            history_record.returned_by = user
            history_record.returned_time = timezone.now()
            history_record.save()
        borrowed_item.delete()
        messages.success(request, 'Item returned successfully!')
    else:
        messages.error(request, 'Item is not borrowed.')
    return redirect('inventory:barcode_scan')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def history(request):
    history_records = History.objects.all().order_by('-borrowed_time')
    return render(request, 'inventory/history.html', {
        'history_records': history_records
    })