from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inventory'

urlpatterns = [
    path('dashboard/', dashborad, name='dashboard'),
    path('add_category/', add_category, name='add_category'),
    path('add_item/', add_item, name='add_item'),
    path('add_user/', add_user, name='add_user'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

