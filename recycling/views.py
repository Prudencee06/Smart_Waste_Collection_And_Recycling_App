from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WasteUploadForm
from .models import WasteUpload

def predict_weight(image, category):
    category_weights = {
        'plastic': 0.3,
        'paper': 0.2,
        'organic': 0.5,
        'metal': 0.7,
    }
    return category_weights.get(category, 0.25)

@login_required
def my_reports_view(request):
    # Fetch all waste uploads for the logged-in user
    uploads = WasteUpload.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'recycling/my_reports.html', {'uploads': uploads})

@login_required
def waste_upload(request):
    if request.method == 'POST':
        form = WasteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            waste = form.save(commit=False)
            waste.user = request.user

            # Predict weight
            waste.predicted_weight = predict_weight(
                waste.image,
                waste.category
            )

            # Calculate points
            waste.points_earned = int(waste.predicted_weight * 10)

            waste.save()

            messages.success(request, "Waste image uploaded successfully!")
            return redirect('accounts:dashboard')
    else:
        form = WasteUploadForm()

    return render(request, 'recycling/waste_upload.html', {'form': form})


def recycling_centers(request):
    centers = [
        {"name": "Green Earth Recycling", "address": "123 Green St, Springfield"},
        {"name": "EcoCycle Center", "address": "456 Eco Ave, Springfield"},
        {"name": "Recycle Hub", "address": "789 Recycle Rd, Springfield"},
    ]
    return render(request, "recycling/centers.html", {"centers": centers})