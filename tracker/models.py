from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

class Intake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField()  # in grams or milliliters
    date = models.DateField(auto_now_add=True)

    def calculate_calories(self):
        return (self.quantity / 100) * self.food.calories_per_100g

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.date}"
    

