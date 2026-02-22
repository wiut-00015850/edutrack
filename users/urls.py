from django.urls import path
from .views import role_redirect, student_dashboard, instructor_dashboard

urlpatterns = [
    path("redirect/", role_redirect, name="role_redirect"),
    path("student/", student_dashboard, name="student_dashboard"),
    path("instructor/", instructor_dashboard, name="instructor_dashboard"),
]