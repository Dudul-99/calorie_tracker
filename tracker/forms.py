# tracker/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Food, Intake
from django.utils import timezone
from .models import CustomUser, CalorieObjective

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['age', 'height', 'weight', 'gender', 'personal_calorie_objective']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget = forms.Select(choices=CalorieObjective.GENDER_CHOICES)
        self.fields['personal_calorie_objective'].widget.attrs['placeholder'] = 'Leave blank to use recommended value'

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.gender and not user.personal_calorie_objective:
            user.calorie_objective = CalorieObjective.objects.get(gender=user.gender)
        if commit:
            user.save()
        return user


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories_per_100g', 'carbohydrates_per_100g', 'fats_per_100g', 'proteins_per_100g', 'is_liquid']


class IntakeForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )

    class Meta:
        model = Intake
        fields = ['food', 'quantity', 'datetime']

