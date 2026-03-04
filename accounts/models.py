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
    
