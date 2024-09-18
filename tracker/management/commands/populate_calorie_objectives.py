# tracker/management/commands/populate_calorie_objectives.py
#python manage.py populate_calorie_objectives
from django.core.management.base import BaseCommand
from tracker.models import CalorieObjective

class Command(BaseCommand):
    help = 'Populate CalorieObjective model with WHO recommendations'

    def handle(self, *args, **kwargs):
        objectives = [
            {'gender': 'M', 'daily_calories': 2500},  # Average for men
            {'gender': 'F', 'daily_calories': 2000},  # Average for women
            {'gender': 'O', 'daily_calories': 2250},  # Average of men and women for 'Other'
        ]

        for obj in objectives:
            CalorieObjective.objects.get_or_create(
                gender=obj['gender'],
                defaults={'daily_calories': obj['daily_calories']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated calorie objectives'))