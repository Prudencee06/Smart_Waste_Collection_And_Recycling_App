from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import Profile, WasteUpload
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import WasteUploadForm
from django.db import models

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
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support.")
        return redirect('home')

    if profile.role == 'municipality':
        return render(request, 'municipality/dashboard.html')

    uploads = WasteUpload.objects.filter(user=request.user).order_by('-created_at')[:5]

    total_points = uploads.aggregate(
        total=models.Sum('points_earned')
    )['total'] or 0

    context = {
        'uploads': uploads,
        'total_points': total_points,
    }

    return render(request, "accounts/dashboard.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def report_waste(request):
    return render(request, "accounts/report_waste.html")  

@login_required
def report_waste(request):
    return render(request, "accounts/report_waste.html") 

@login_required
def my_reports(request):
    return render(request, "accounts/my_reports.html")

@login_required
def view_reports(request):
    return render(request, "municipality/view_reports.html")

@login_required
def analytics(request):
    return render(request, "municipality/analytics.html")

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

#waste upload
@login_required
def waste_upload(request):
    if request.method == 'POST':
        form = WasteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            waste_upload = form.save(commit=False)
            waste_upload.user = request.user

            #prediction(waste category + weights)
            waste_upload.predicted_weight = predicted_weight(
                waste_upload.image,
                waste_upload.category
            ) 

            #points
            waste_upload.points_earned = int(waste_upload.predicted_weight * 10)

            waste_upload.save()
            messages.success(request, "Waste image uploaded successfully!")
            return redirect('accounts/dashboard')
        else:
            form = WasteUploadForm()
    return render(request, 'accounts/my_reports.html', {'form': form})

# waste predistion testing
def predict_weight(image, category):
    # TEMPORARY logic (replace with ML later)
    category_weights = {
        'plastic': 0.3,
        'paper': 0.2,
        'organic': 0.5,
        'metal': 0.7,
    }
    return category_weights.get(category, 0.25)