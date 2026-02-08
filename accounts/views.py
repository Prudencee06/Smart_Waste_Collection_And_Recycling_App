from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                # role-based redirect
                role = user.profile.role
                if role == "citizen":
                    return redirect("user_dashboard")
                elif role == "municipality":
                    return redirect("municipality_dashboard")
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
            return redirect("login")

    return render(request, "accounts/register.html", {"form": form})


@login_required
def user_dashboard(request):
    return render(request, "accounts/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")
