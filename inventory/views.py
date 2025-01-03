from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .forms import LoginForm
from django.http import HttpResponseForbidden
from .models import *

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('inventory_dashboard')  # Replace with your inventory dashboard URL
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'inventory/login.html', {'form': form})

def dashboard_view(request):
    return render(request, 'inventory/dashboard.html', {"user": request.user})

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        Category.objects.create(name=category_name)
        messages.success(request, "Item added successfully!")
        return redirect('dashboard')
    return render(request, 'inventory/add_category.html')

def add_item(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        quantity = request.POST.get('quantity')
        Item.objects.create(name=name, category_id=category_id, quantity=quantity)
        messages.success(request, "Item added successfully!")
        return redirect('dashboard')
    return render(request, 'inventory/add_item.html')

def add_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        team = request.POST.get('team')
        User.objects.create(first_name=first_name, last_name=last_name, gender=gender, email=email, birth_date=birth_date, team=team)
        messages.success(request, "User added successfully!")
        return redirect('dashboard')
    return render(request, 'inventory/add_user.html')