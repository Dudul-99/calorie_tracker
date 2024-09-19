#python manage.py test
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CalorieObjective

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.calorie_objective = CalorieObjective.objects.create(gender='M', daily_calories=2500)

    def test_create_user(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_get_daily_calorie_objective(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            gender='M',
            calorie_objective=self.calorie_objective
        )
        self.assertEqual(user.get_daily_calorie_objective(), 2500)

    def test_calculate_bmi(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            height=180,
            weight=75
        )
        self.assertAlmostEqual(user.calculate_bmi(), 23.15, places=2)



