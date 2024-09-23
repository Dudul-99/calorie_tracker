from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Food, Intake, CalorieObjective
from tracker.forms import UserRegistrationForm, UserProfileForm, FoodForm, IntakeForm
from django.urls import reverse


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.food = Food.objects.create(name='Apple', calories_per_100g=52, carbohydrates_per_100g=14,
                                        fats_per_100g=0.2, proteins_per_100g=0.3, is_liquid=False)

    def test_home_view(self):
        response = self.client.get(reverse('tracker:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/home.html')

    def test_add_food_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tracker:add_food'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/add_food.html')

    def test_add_intake_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tracker:add_intake'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/add_intake.html')

    def test_calorie_summary_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tracker:calorie_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/calorie_summary.html')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tracker:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/edit_profile.html')
