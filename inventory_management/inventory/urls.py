from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'inventory'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('adding/', add, name='add'),
    path('display/', display, name='display'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('delete_item/<str:item_id>/', views.delete_item, name='delete_item'),
    path('add_user/', add_user, name='add_user'),
    path('profile/', profile, name='profile'),
    path('display_user/', display_user, name='display_users'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('barcode_scan/', views.barcode_scan, name='barcode_scan'),
    path('borrow_item/<str:item_id>/', views.borrow_item, name='borrow_item'),
    path('return_item/<str:item_id>/', views.return_item, name='return_item'),
    path('history/', views.history, name='history'),
]

