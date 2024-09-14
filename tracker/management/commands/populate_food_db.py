from django.core.management.base import BaseCommand
from tracker.models import Food

class Command(BaseCommand):
    help = 'Populate the database with initial food data'

    def handle(self, *args, **kwargs):
        foods = [
            {'name': 'Apple', 'calories_per_100g': 52, 'is_liquid': False},
            {'name': 'Banana', 'calories_per_100g': 89, 'is_liquid': False},
            {'name': 'Chicken Breast', 'calories_per_100g': 165, 'is_liquid': False},
            {'name': 'Whole Milk', 'calories_per_100g': 61, 'is_liquid': True},
            {'name': 'Egg', 'calories_per_100g': 155, 'is_liquid': False},
            {'name': 'Salmon', 'calories_per_100g': 206, 'is_liquid': False},
            {'name': 'Quinoa', 'calories_per_100g': 120, 'is_liquid': False},
            {'name': 'Haddock (Eglefin)', 'calories_per_100g': 90, 'is_liquid': False},
            {'name': 'Tofu', 'calories_per_100g': 76, 'is_liquid': False},
            {'name': 'Greek Yogurt', 'calories_per_100g': 59, 'is_liquid': False},
            # Add more foods as needed
        ]

        for food_data in foods:
            Food.objects.create(**food_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated food database'))

        for food_data in foods:
            Food.objects.create(**food_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated food database'))

