from django.urls import path
from . import views

urlpatterns = [
    path("<int:assignment_id>/", views.assignment_detail, name="assignment_detail"),
    path(
        "<int:assignment_id>/instructor/",
        views.instructor_assignment_detail,
        name="instructor_assignment_detail",
    ),
    path(
        "create/<int:course_id>/",
        views.create_assignment,
        name="create_assignment",
    ),
]