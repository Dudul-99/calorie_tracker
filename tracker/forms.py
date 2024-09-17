from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Food, Intake

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'is_liquid']

class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['food', 'quantity']
