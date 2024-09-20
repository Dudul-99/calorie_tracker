# tracker/tests/test_models.py

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tracker.models import Food, Intake, CalorieObjective
from tracker.forms import UserRegistrationForm, UserProfileForm, FoodForm, IntakeForm
from django.urls import reverse

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



# Forms tests
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


# Views tests
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


# Integration tests
