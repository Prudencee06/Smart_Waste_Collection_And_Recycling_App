from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, "municipality/dashboard.html")  

@login_required
def view_reports(request):
    return render(request, "municipality/view_reports.html") 

@login_required
def analytics(request):
    return render(request, "municipality/analytics.html")  
