from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from users.models import Profile
from users.decorators import instructor_required
from courses.models import Course
from assignments.models import Assignment


@login_required
def role_redirect(request):
    role = request.user.profile.role

    if role == Profile.Role.STUDENT:
        return redirect("student_dashboard")
    elif role == Profile.Role.INSTRUCTOR:
        return redirect("instructor_dashboard")

    return render(request, "users/invalid_role.html", status=403)


@login_required
def student_dashboard(request):
    profile = request.user.profile

    if profile.role != Profile.Role.STUDENT:
        return HttpResponseForbidden("You are not allowed to access this page")

    courses = Course.objects.filter(students=request.user)
    assignments = Assignment.objects.filter(course__in=courses).order_by("due_date")

    return render(
        request,
        "users/student_dashboard.html",
        {
            "courses": courses,
            "assignments": assignments,
        },
    )


@login_required
@instructor_required
def instructor_dashboard(request):
    return render(request, "users/instructor_dashboard.html")