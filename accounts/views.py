from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum
from recycling.models import WasteUpload
from municipality.models import NewsItem


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                role = user.profile.role
                if role == "citizen":
                    return redirect("accounts:dashboard")
                elif role == "municipality":
                    return redirect("municipality:dashboard")
            else:
                messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == 'municipality':
        return render(request, 'municipality/dashboard.html')

    #Now pulling uploads from recycling app
    # Collected trash (just take all uploads for the user)
    uploads = WasteUpload.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Pending trash (maybe small weight uploads not yet collected)
    pending_uploads = WasteUpload.objects.filter(user=request.user, predicted_weight=0).order_by('-created_at')

    # Total points
    total_points = WasteUpload.objects.filter(user=request.user).aggregate(total=Sum('points_earned'))['total'] or 0

    # News items from municipality
    news_items = NewsItem.objects.order_by('-created_at')[:6]

    context = {
        'uploads': uploads,
        'pending_uploads': pending_uploads,
        'total_points': total_points,
        'news_items': news_items,
    }

    return render(request, "accounts/dashboard.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile(request):
    return render(request, "accounts/profile.html")