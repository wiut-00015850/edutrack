from django.conf import settings
from django.db import models
from assignments.models import User


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"