from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


class Assignment(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        return self.due_date < timezone.now()

    @property
    def is_due_soon(self):
        now = timezone.now()
        return now <= self.due_date <= now + timedelta(days=3)

    @property
    def status(self):
        if self.is_overdue:
            return "overdue"
        if self.is_due_soon:
            return "due-soon"
        return "upcoming"

    def __str__(self):
        return f"{self.title} ({self.course})"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    file = models.FileField(upload_to="submissions/")
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("assignment", "student")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student} → {self.assignment}"