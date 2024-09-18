from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create of models here.

class CalorieObjective(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, unique=True)
    daily_calories = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_gender_display()} - {self.daily_calories} calories"




class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    calorie_objective = models.ForeignKey('CalorieObjective', on_delete=models.SET_NULL, null=True, blank=True)
    personal_calorie_objective = models.PositiveIntegerField(null=True, blank=True)

    def get_daily_calorie_objective(self):
        if self.personal_calorie_objective:
            return self.personal_calorie_objective
        return self.calorie_objective.daily_calories if self.calorie_objective else None

    
    def calculate_bmi(self):
        if self.height and self.weight:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None

    def __str__(self):
        return self.username


class Food(models.Model):
    name = models.CharField(max_length=100)
    calories_per_100g = models.FloatField()
    carbohydrates_per_100g = models.FloatField()
    fats_per_100g = models.FloatField()
    proteins_per_100g = models.FloatField()
    is_liquid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


User = get_user_model()

class Intake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity in grams or milliliters")
    datetime = models.DateTimeField(default=timezone.now)

    def calculate_calories(self):
        return (self.quantity / 100) * self.food.calories_per_100g

    def calculate_nutrients(self):
        factor = self.quantity / 100
        return {
            'calories': factor * self.food.calories_per_100g,
            'carbs': factor * self.food.carbohydrates_per_100g,
            'fats': factor * self.food.fats_per_100g,
            'proteins': factor * self.food.proteins_per_100g
        }

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.datetime}"


