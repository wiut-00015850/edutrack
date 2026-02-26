from django.urls import path
from . import views

urlpatterns = [
    path("<int:course_id>/", views.course_detail, name="course_detail"),
    path("create/", views.create_course, name="create_course"),
    path("available/", views.available_courses, name="available_courses"),
    path("<int:course_id>/enroll/", views.enroll_course, name="enroll_course"),
    path("<int:course_id>/leave/", views.leave_course, name="leave_course"),
    path("<int:course_id>/lessons/create/", views.create_lesson, name="create_lesson"),
]

