# tracker/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from .models import Food, Intake, CustomUser
from .forms import FoodForm, IntakeForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import CustomUser
from datetime import timedelta

def home(request):
    return render(request, 'tracker/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Calorie Tracker account.'
            message = render_to_string('tracker/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'tracker/email_confirmation_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('tracker:home')
    else:
        return render(request, 'tracker/activation_invalid.html')

@login_required
def view_profile(request):
    user = request.user
    bmi = user.calculate_bmi()
    return render(request, 'tracker/view_profile.html', {'user': user, 'bmi': bmi})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('tracker:view_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'tracker/edit_profile.html', {'form': form})



# Keep your existing add_food, add_intake, and calorie_summary views here
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
            messages.success(request, 'Intake recorded successfully.')
            return redirect('tracker:calorie_summary')
    else:
        form = IntakeForm()
    return render(request, 'tracker/add_intake.html', {'form': form})

@login_required
def calorie_summary(request):
    date = request.GET.get('date')
    if date:
        date = timezone.datetime.strptime(date, "%Y-%m-%d").date()
    else:
        date = timezone.now().date()

    next_day = date + timedelta(days=1)
    intakes = Intake.objects.filter(
        user=request.user,
        datetime__gte=date,
        datetime__lt=next_day
    ).order_by('datetime')

    total_nutrients = {
        'calories': sum(intake.calculate_nutrients()['calories'] for intake in intakes),
        'carbs': sum(intake.calculate_nutrients()['carbs'] for intake in intakes),
        'fats': sum(intake.calculate_nutrients()['fats'] for intake in intakes),
        'proteins': sum(intake.calculate_nutrients()['proteins'] for intake in intakes)
    }

    context = {
        'date': date,
        'intakes': intakes,
        'total_nutrients': total_nutrients,
    }
    return render(request, 'tracker/calorie_summary.html', context)