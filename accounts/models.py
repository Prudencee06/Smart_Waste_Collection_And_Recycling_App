from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ("citizen", "Citizen"),
        ("municipality", "Municipality"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
# waste upload model
class WasteUpload(models.Model):
    Waste_Categories = [
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/waste_uploads/')
    category = models.CharField(max_length=20, choices=Waste_Categories)
    # predicted_weight = models.FloatField(help_text="Weight in kg")
    predicted_weight = models.FloatField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
