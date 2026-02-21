from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_taught",
    )
    students = models.ManyToManyField(
        User,
        related_name="courses_enrolled",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title