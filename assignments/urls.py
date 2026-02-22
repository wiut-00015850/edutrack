from django.urls import path
from .views import submit_assignment

urlpatterns = [
    path("submit/", submit_assignment, name="submit_assignment"),
]