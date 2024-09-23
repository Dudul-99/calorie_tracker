from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from tracker.models import Food, Intake, CalorieObjective

class IntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.food = Food.objects.create(
            name='Apple', 
            calories_per_100g=52,
            proteins_per_100g=0.3,
            carbohydrates_per_100g=14,
            fats_per_100g=0.2
        )
        CalorieObjective.objects.create(gender='M', daily_calories=2500)

    def test_user_registration_and_profile_edit(self):
        # Register a new user
        response = self.client.post(reverse('tracker:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        print("Registration response status:", response.status_code)
        print("Registration response content:", response.content.decode())

        # Check if user was created
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

        # Simulate email verification (you might need to adjust this based on your implementation)
        new_user = get_user_model().objects.get(username='newuser')
        new_user.is_active = True
        new_user.save()

        # Login with the new user
        login_successful = self.client.login(username='newuser', password='newpassword123')
        self.assertTrue(login_successful)

        # Edit profile
        response = self.client.post(reverse('tracker:edit_profile'), {
            'age': 25,
            'height': 180,
            'weight': 75,
            'gender': 'M',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit

        # Check if profile was updated
        user = get_user_model().objects.get(username='newuser')
        self.assertEqual(user.age, 25)
        self.assertEqual(user.height, 180)
        self.assertEqual(user.weight, 75)
        self.assertEqual(user.gender, 'M')

    def test_food_intake_and_calorie_summary(self):
        self.client.login(username='testuser', password='testpass123')

        # Add a food intake for today
        today = timezone.now().date()
        response = self.client.post(reverse('tracker:add_intake'), {
            'food': self.food.id,
            'quantity': 200,
            'datetime': today.strftime('%Y-%m-%d 12:00:00'),
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful addition

        # Check calorie summary
        response = self.client.get(reverse('tracker:calorie_summary'))
        self.assertEqual(response.status_code, 200)
        print("Calorie summary response content:", response.content.decode())
        
        # Check if the intake is recorded
        self.assertContains(response, 'Apple')
        self.assertContains(response, '104')  # 52 calories per 100g * 200g = 104 calories

        # Print all intakes for debugging
        all_intakes = Intake.objects.all()
        for intake in all_intakes:
            print(f"Intake: {intake.food.name}, Quantity: {intake.quantity}, DateTime: {intake.datetime}")