from django import forms
from assignments.models import Submission
from .models import Assignment


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date"]