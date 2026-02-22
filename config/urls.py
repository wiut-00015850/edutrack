from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import health_check

urlpatterns = [
    # PUBLIC
    path("login/", auth_views.LoginView.as_view(
        template_name="auth/login.html"
    ), name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("health/", health_check, name="health"),

    # APPS
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("courses/", include("courses.urls")),
    path("assignments/", include("assignments.urls")),
]