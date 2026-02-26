from django import forms
from assignments.models import Submission
from .models import Assignment

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date"]