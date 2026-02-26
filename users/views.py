from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from users.models import Profile
from users.decorators import instructor_required
from courses.models import Course
from assignments.models import Assignment, Submission


@login_required
def role_redirect(request):
    if request.user.is_superuser:
        return redirect("/admin/")

    role = request.user.profile.role

    if role == Profile.Role.STUDENT:
        return redirect("student_dashboard")

    if role == Profile.Role.INSTRUCTOR:
        return redirect("instructor_dashboard")

    return HttpResponseForbidden("Invalid role")


@login_required
def student_dashboard(request):
    if request.user.profile.role != Profile.Role.STUDENT:
        return HttpResponseForbidden("You are not allowed to access this page")

    courses = (
        Course.objects
        .filter(students=request.user)
        .distinct()
    )

    assignments = (
        Assignment.objects
        .filter(course__in=courses)
        .exclude(submissions__student=request.user)
        .order_by("due_date")
    )
    

    return render(
        request,
        "users/student_dashboard.html",
        {
            "courses": courses,
            "assignments": assignments,
        }
    )


@login_required
@instructor_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)

    return render(
        request,
        "users/instructor_dashboard.html",
        {
            "courses": courses,
        }
    )

