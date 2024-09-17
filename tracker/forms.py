# tracker/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Food, Intake

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'height', 'weight', 'gender']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'carbohydrates_per_100g', 'fats_per_100g', 'proteins_per_100g', 'is_liquid']

class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['food', 'quantity']
