from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Food, Intake, CalorieObjective
from tracker.forms import UserRegistrationForm, UserProfileForm, FoodForm, IntakeForm


class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid_data(self):
        form = UserRegistrationForm(data={
            'username': '',
            'email': 'invalid_email',
            'password1': 'short',
            'password2': 'short',
        })
        self.assertFalse(form.is_valid())

class UserProfileFormTest(TestCase):
    def test_user_profile_form_valid_data(self):
        form = UserProfileForm(data={
            'age': 25,
            'height': 180,
            'weight': 75,
            'gender': 'M',
            'personal_calorie_objective': 2500,
        })
        self.assertTrue(form.is_valid())

class FoodFormTest(TestCase):
    def test_food_form_valid_data(self):
        form = FoodForm(data={
            'name': 'Banana',
            'calories_per_100g': 89,
            'carbohydrates_per_100g': 23,
            'fats_per_100g': 0.3,
            'proteins_per_100g': 1.1,
            'is_liquid': False,
        })
        self.assertTrue(form.is_valid())

class IntakeFormTest(TestCase):
    def setUp(self):
        self.food = Food.objects.create(name='Apple', calories_per_100g=52, carbohydrates_per_100g=14,
                                        fats_per_100g=0.2, proteins_per_100g=0.3, is_liquid=False)

    def test_intake_form_valid_data(self):
        form = IntakeForm(data={
            'food': self.food.id,
            'quantity': 150,
            'datetime': '2023-01-01 12:00:00',
        })
        self.assertTrue(form.is_valid())