from django.urls import path
from . import views
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('add_category/', views.add_category, name='add_category'),
]

urlpatterns += [
    path('dashboard/', dashboard_view, name='inventory_dashboard'),
]
