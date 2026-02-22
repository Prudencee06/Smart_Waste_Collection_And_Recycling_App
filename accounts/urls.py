from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("report-waste/", views.report_waste, name="report_waste"),
    path("waste-upload/", views.waste_upload, name="waste_upload"),
    path("profile/", views.profile, name="profile"),
]
