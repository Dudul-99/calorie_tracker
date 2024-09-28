from django.core.management.base import BaseCommand
from tracker.models import Food

class Command(BaseCommand):
    help = 'Populate the database with initial food data'

    def handle(self, *args, **kwargs):
        foods = [
            {'name': 'Almonds', 'calories_per_100g': 579, 'carbohydrates_per_100g': 21.6, 'fats_per_100g': 49.9, 'proteins_per_100g': 21.2, 'is_liquid': False},
            {'name': 'Apple', 'calories_per_100g': 52, 'carbohydrates_per_100g': 13.8, 'fats_per_100g': 0.2, 'proteins_per_100g': 0.3, 'is_liquid': False},
            {'name': 'Banana', 'calories_per_100g': 89, 'carbohydrates_per_100g': 22.8, 'fats_per_100g': 0.3, 'proteins_per_100g': 1.1, 'is_liquid': False},
            {'name': 'Broccoli', 'calories_per_100g': 34, 'carbohydrates_per_100g': 6.6, 'fats_per_100g': 0.4, 'proteins_per_100g': 2.8, 'is_liquid': False},
            {'name': 'Brown Rice', 'calories_per_100g': 111, 'carbohydrates_per_100g': 23, 'fats_per_100g': 0.9, 'proteins_per_100g': 2.6, 'is_liquid': False},
            {'name': 'Chicken Breast', 'calories_per_100g': 165, 'carbohydrates_per_100g': 0, 'fats_per_100g': 3.6, 'proteins_per_100g': 31, 'is_liquid': False},
            {'name': 'Chickpeas', 'calories_per_100g': 164, 'carbohydrates_per_100g': 27.4, 'fats_per_100g': 2.6, 'proteins_per_100g': 8.9, 'is_liquid': False},
            {'name': 'Chopped Steak', 'calories_per_100g': 250, 'carbohydrates_per_100g': 0, 'fats_per_100g': 20, 'proteins_per_100g': 19, 'is_liquid': False},
            {'name': 'Egg', 'calories_per_100g': 155, 'carbohydrates_per_100g': 1.1, 'fats_per_100g': 10.6, 'proteins_per_100g': 12.6, 'is_liquid': False},
            {'name': 'Greek Yogurt', 'calories_per_100g': 59, 'carbohydrates_per_100g': 3.6, 'fats_per_100g': 0.4, 'proteins_per_100g': 10, 'is_liquid': False},
            {'name': 'Haddock', 'calories_per_100g': 90, 'carbohydrates_per_100g': 0, 'fats_per_100g': 0.9, 'proteins_per_100g': 20.6, 'is_liquid': False},
            {'name': 'Lentils', 'calories_per_100g': 116, 'carbohydrates_per_100g': 20, 'fats_per_100g': 0.4, 'proteins_per_100g': 9, 'is_liquid': False},
            {'name': 'Meat', 'calories_per_100g': 143, 'carbohydrates_per_100g': 0, 'fats_per_100g': 5.4, 'proteins_per_100g': 21.2, 'is_liquid': False},
            {'name': 'Olive Oil', 'calories_per_100g': 884, 'carbohydrates_per_100g': 0, 'fats_per_100g': 100, 'proteins_per_100g': 0, 'is_liquid': True},
            {'name': 'Oats', 'calories_per_100g': 389, 'carbohydrates_per_100g': 66.3, 'fats_per_100g': 6.9, 'proteins_per_100g': 16.9, 'is_liquid': False},
            {'name': 'Orange', 'calories_per_100g': 47, 'carbohydrates_per_100g': 11.8, 'fats_per_100g': 0.1, 'proteins_per_100g': 0.9, 'is_liquid': False},
            {'name': 'Pasta', 'calories_per_100g': 131, 'carbohydrates_per_100g': 25, 'fats_per_100g': 1.1, 'proteins_per_100g': 5, 'is_liquid': False},
            {'name': 'Quinoa', 'calories_per_100g': 120, 'carbohydrates_per_100g': 21.3, 'fats_per_100g': 1.9, 'proteins_per_100g': 4.4, 'is_liquid': False},
            {'name': 'Salmon', 'calories_per_100g': 206, 'carbohydrates_per_100g': 0, 'fats_per_100g': 13.4, 'proteins_per_100g': 22.1, 'is_liquid': False},
            {'name': 'Spinach', 'calories_per_100g': 23, 'carbohydrates_per_100g': 3.6, 'fats_per_100g': 0.4, 'proteins_per_100g': 2.9, 'is_liquid': False},
            {'name': 'Sweet Potato', 'calories_per_100g': 86, 'carbohydrates_per_100g': 20.1, 'fats_per_100g': 0.1, 'proteins_per_100g': 1.6, 'is_liquid': False},
            {'name': 'Tofu', 'calories_per_100g': 76, 'carbohydrates_per_100g': 1.9, 'fats_per_100g': 4.8, 'proteins_per_100g': 8, 'is_liquid': False},
            {'name': 'Whole Milk', 'calories_per_100g': 61, 'carbohydrates_per_100g': 4.8, 'fats_per_100g': 3.3, 'proteins_per_100g': 3.2, 'is_liquid': True},
        ]

        for food_data in foods:
            Food.objects.create(**food_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated food database'))
