from django import forms
from .models import Course, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Course title",
            }),
            "description": forms.Textarea(attrs={
                "class": "textarea",
                "placeholder": "Short course description",
                "rows": 4,
            }),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "video"]

