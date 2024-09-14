from django import forms
from .models import Food, Intake

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'is_liquid']

class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['food', 'quantity']
