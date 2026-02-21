from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("INSTRUCTOR", "Instructor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user} ({self.role})"