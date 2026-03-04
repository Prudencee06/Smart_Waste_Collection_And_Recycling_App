from django.db import models
from django.contrib.auth.models import User

class WasteUpload(models.Model):
    WASTE_CATEGORIES = [
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='waste_uploads/')
    category = models.CharField(max_length=20, choices=WASTE_CATEGORIES)
    predicted_weight = models.FloatField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
    

