from django.contrib import admin
from django.urls import path
from .views import health_check
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import health_check, home


def root_redirect(request):
    return redirect("login")

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),

    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]
