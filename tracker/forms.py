from django import forms
from .models import Food, Intake
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'is_liquid']

class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['food', 'quantity']
