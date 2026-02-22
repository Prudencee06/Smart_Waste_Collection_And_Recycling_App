from django.urls import path
from . import views

app_name = "municipality"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("view-reports/", views.view_reports, name="view_reports"),
    path("analytics/", views.analytics, name="analytics"),
]
