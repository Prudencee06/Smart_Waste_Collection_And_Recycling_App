from django import forms
from .models import WasteUpload

class WasteUploadForm(forms.ModelForm):
    class Meta:
        model = WasteUpload
        fields = ['image', 'category']