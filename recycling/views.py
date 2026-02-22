from django.shortcuts import render

# Create your views here.
def recycling_centers(request):
    # In a real application, you'd fetch this data from the database
    centers = [
        {"name": "Green Earth Recycling", "address": "123 Green St, Springfield"},
        {"name": "EcoCycle Center", "address": "456 Eco Ave, Springfield"},
        {"name": "Recycle Hub", "address": "789 Recycle Rd, Springfield"},
    ]
    return render(request, "recycling/centers.html", {"centers": centers})