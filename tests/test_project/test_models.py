from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Food, Intake, CalorieObjective

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




class FoodModelTest(TestCase):
    def test_create_food(self):
        food = Food.objects.create(
            name='Apple',
            calories_per_100g=52,
            carbohydrates_per_100g=14,
            fats_per_100g=0.2,
            proteins_per_100g=0.3,
            is_liquid=False
        )
        self.assertEqual(food.name, 'Apple')
        self.assertEqual(food.calories_per_100g, 52)

class IntakeModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.food = Food.objects.create(name='Apple', calories_per_100g=52,
                                        carbohydrates_per_100g=14, fats_per_100g=0.2, proteins_per_100g=0.3,
                                        is_liquid=False)

    def test_create_intake(self):
        intake = Intake.objects.create(
            user=self.user,
            food=self.food,
            quantity=150
        )
        self.assertEqual(intake.user, self.user)
        self.assertEqual(intake.food, self.food)
        self.assertEqual(intake.quantity, 150)

    def test_calculate_calories(self):
        intake = Intake.objects.create(
            user=self.user,
            food=self.food,
            quantity=150
        )
        self.assertAlmostEqual(intake.calculate_calories(), 78, places=2)


class CalorieObjectiveModelTest(TestCase):
    def test_create_calorie_objective(self):
        objective = CalorieObjective.objects.create(
            gender='F',
            daily_calories=2000
        )
        self.assertEqual(objective.gender, 'F')
        self.assertEqual(objective.daily_calories, 2000)

