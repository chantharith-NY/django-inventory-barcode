from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import UserProfile

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "inventory/login.html")

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        if Category.objects.filter(name=category_name).exists():
            messages.error(request, "Category already exists!")
        else:
            category = Category.objects.create(name=category_name, description=description)
            category.save()
            messages.success(request, "Category added successfully!")
        return redirect('inventory:dashboard')
    return render(request, 'inventory/add_category.html')

@login_required
@user_passes_test(is_admin)
def add_item(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')
        Item.objects.create(name=name, category_id=category_id, quantity=quantity)
        messages.success(request, "Item added successfully!")
        return redirect('inventory:dashboard')
    return render(request, 'inventory/add_item.html')

@login_required
def dashborad(request):
    user = request.user
    items = Item.objects.all()
    return render(request, 'inventory/dashboard.html', {
        'items': items,
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL,
    })

@login_required
def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = '12345'
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        team = request.POST.get('team')
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=password, gender=gender, email=email, birth_date=birth_date, team=team)
        user.gender = gender
        user.birth_date = birth_date
        user.team = team
        user.save()
        messages.success(request, "User added successfully!")
        return redirect('inventory:dashboard')
    return render(request, 'inventory/add_user.html')
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@login_required
def profile(request):
    user = request.user
    return render(request, 'inventory/profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.gender = request.POST.get('gender')
        user.birth_date = request.POST.get('birth_date')
        user.team = request.POST.get('team')
        user.save()
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('inventory:profile')
    return render(request, 'inventory/edit_profile.html', {'user': user, 'profile': profile})
        
@login_required
def profile(request):
    user = request.user
    return render(request, 'inventory/profile.html', {'user': user})
