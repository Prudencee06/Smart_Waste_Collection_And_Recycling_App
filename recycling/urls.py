from django.urls import path
from . import views

app_name = 'recycling'

urlpatterns = [
    path("report-waste/", views.waste_upload, name="waste_upload"),  
    path("my-reports/", views.my_reports_view, name="my_reports"),  
    path("centers/", views.recycling_centers, name="centers"),
]
