from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from .models import Food, Intake
from .forms import FoodForm, IntakeForm, UserRegistrationForm

def home(request):
    return render(request, 'tracker/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracker:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:home')
    else:
        form = FoodForm()
    return render(request, 'tracker/add_food.html', {'form': form})

@login_required
def add_intake(request):
    if request.method == 'POST':
        form = IntakeForm(request.POST)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            return redirect('tracker:calorie_summary')
    else:
        form = IntakeForm()
    return render(request, 'tracker/add_intake.html', {'form': form})

@login_required
def calorie_summary(request):
    today_intakes = Intake.objects.filter(user=request.user, date=timezone.now().date())
    total_calories = sum(intake.calculate_calories() for intake in today_intakes)
    return render(request, 'tracker/calorie_summary.html', {
        'total_calories': total_calories,
        'intakes': today_intakes
    })