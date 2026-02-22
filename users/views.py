from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

@login_required
def role_redirect(request):
    profile = getattr(request.user, "profile", None)

    if not profile:
        return redirect(settings.LOGIN_URL)

    role = profile.role.lower()

    if role == "student":
        return redirect("student_dashboard")

    if role == "instructor":
        return redirect("instructor_dashboard")

    return HttpResponse("Invalid user role", status=403)


@login_required
def student_dashboard(request):
    return HttpResponse("Student dashboard")


@login_required
def instructor_dashboard(request):
    return HttpResponse("Instructor dashboard")