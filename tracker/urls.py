from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('add_food/', views.add_food, name='add_food'),
    path('add_intake/', views.add_intake, name='add_intake'),
    path('summary/', views.calorie_summary, name='calorie_summary'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]